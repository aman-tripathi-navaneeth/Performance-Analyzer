"""
SIS (Student Information System) Integration Service
Handles external college portal integration for backlog checking
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, Optional, List
import re
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class SISIntegration:
    """Service to integrate with college SIS portal"""
    
    def __init__(self):
        self.base_url = "https://sis.idealtech.edu.in"
        self.login_url = f"{self.base_url}/student/index.php"
        self.session = requests.Session()
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def login_student(self, roll_number: str, password: str) -> bool:
        """
        Login to SIS portal with student credentials
        
        Args:
            roll_number: Student roll number
            password: Student password (assuming same as roll number for now)
            
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            # First, get the login page to extract any CSRF tokens or form data
            login_page = self.session.get(self.login_url, timeout=10)
            login_page.raise_for_status()
            
            soup = BeautifulSoup(login_page.content, 'html.parser')
            
            # Find the login form
            login_form = soup.find('form')
            if not login_form:
                logger.error("Login form not found on SIS portal")
                return False
            
            # Extract form action and method
            form_action = login_form.get('action', '')
            form_method = login_form.get('method', 'post').lower()
            
            # Build the full URL for form submission
            if form_action:
                submit_url = urljoin(self.login_url, form_action)
            else:
                submit_url = self.login_url
            
            # Prepare login data
            login_data = {
                'username': roll_number,
                'password': password,
                'roll_number': roll_number,
                'student_id': roll_number,
                'login': 'Login',
                'submit': 'Login'
            }
            
            # Add any hidden form fields (CSRF tokens, etc.)
            hidden_inputs = soup.find_all('input', type='hidden')
            for hidden_input in hidden_inputs:
                name = hidden_input.get('name')
                value = hidden_input.get('value', '')
                if name:
                    login_data[name] = value
            
            # Submit login form
            if form_method == 'get':
                response = self.session.get(submit_url, params=login_data, timeout=10)
            else:
                response = self.session.post(submit_url, data=login_data, timeout=10)
            
            response.raise_for_status()
            
            # Check if login was successful
            # Look for indicators of successful login (dashboard, student name, etc.)
            response_text = response.text.lower()
            
            # Common indicators of successful login
            success_indicators = [
                'dashboard', 'welcome', 'student portal', 'logout', 
                'profile', 'results', 'academic', roll_number.lower()
            ]
            
            # Common indicators of failed login
            failure_indicators = [
                'invalid', 'error', 'incorrect', 'failed', 'try again',
                'username or password', 'login failed'
            ]
            
            # Check for failure indicators first
            for indicator in failure_indicators:
                if indicator in response_text:
                    logger.warning(f"Login failed for {roll_number}: Found failure indicator '{indicator}'")
                    return False
            
            # Check for success indicators
            for indicator in success_indicators:
                if indicator in response_text:
                    logger.info(f"Login successful for {roll_number}")
                    return True
            
            # If no clear indicators, check response URL
            if 'login' not in response.url.lower() and response.url != self.login_url:
                logger.info(f"Login appears successful for {roll_number} (redirected to {response.url})")
                return True
            
            logger.warning(f"Login status unclear for {roll_number}")
            return False
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during login for {roll_number}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during login for {roll_number}: {str(e)}")
            return False
    
    def get_student_results(self, roll_number: str) -> Optional[Dict]:
        """
        Fetch student results and analyze backlogs
        
        Args:
            roll_number: Student roll number
            
        Returns:
            Dict containing backlog information or None if failed
        """
        try:
            # Look for results/grades page
            possible_results_urls = [
                f"{self.base_url}/student/results.php",
                f"{self.base_url}/student/grades.php",
                f"{self.base_url}/student/academic.php",
                f"{self.base_url}/student/transcript.php",
                f"{self.base_url}/results.php",
                f"{self.base_url}/grades.php"
            ]
            
            results_data = None
            
            for url in possible_results_urls:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Look for tables containing results
                        tables = soup.find_all('table')
                        if tables:
                            results_data = self._parse_results_table(soup, roll_number)
                            if results_data:
                                break
                                
                except requests.exceptions.RequestException:
                    continue
            
            if not results_data:
                # Try to find results in the main dashboard
                dashboard_response = self.session.get(f"{self.base_url}/student/", timeout=10)
                if dashboard_response.status_code == 200:
                    soup = BeautifulSoup(dashboard_response.content, 'html.parser')
                    results_data = self._parse_results_table(soup, roll_number)
            
            return results_data
            
        except Exception as e:
            logger.error(f"Error fetching results for {roll_number}: {str(e)}")
            return None
    
    def _parse_results_table(self, soup: BeautifulSoup, roll_number: str) -> Optional[Dict]:
        """
        Parse HTML tables to extract results and calculate backlogs
        
        Args:
            soup: BeautifulSoup object of the page
            roll_number: Student roll number for logging
            
        Returns:
            Dict containing parsed results data
        """
        try:
            results = {
                'roll_number': roll_number,
                'total_subjects': 0,
                'passed_subjects': 0,
                'failed_subjects': 0,
                'backlogs': [],
                'overall_percentage': 0,
                'cgpa': 0,
                'semester_results': []
            }
            
            # Look for results tables
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) < 2:  # Skip tables with no data rows
                    continue
                
                # Check if this looks like a results table
                header_row = rows[0]
                headers = [th.get_text().strip().lower() for th in header_row.find_all(['th', 'td'])]
                
                # Common column names in results tables
                result_indicators = ['subject', 'marks', 'grade', 'result', 'status', 'semester']
                
                if any(indicator in ' '.join(headers) for indicator in result_indicators):
                    # This looks like a results table
                    for row in rows[1:]:  # Skip header row
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 3:  # Minimum columns for meaningful data
                            
                            row_data = [cell.get_text().strip() for cell in cells]
                            
                            # Try to extract subject and result information
                            subject_info = self._extract_subject_info(row_data, headers)
                            if subject_info:
                                results['total_subjects'] += 1
                                
                                if subject_info['status'].lower() in ['pass', 'passed', 'p']:
                                    results['passed_subjects'] += 1
                                elif subject_info['status'].lower() in ['fail', 'failed', 'f', 'backlog']:
                                    results['failed_subjects'] += 1
                                    results['backlogs'].append(subject_info)
                                
                                results['semester_results'].append(subject_info)
            
            # Calculate overall statistics
            if results['total_subjects'] > 0:
                results['pass_percentage'] = (results['passed_subjects'] / results['total_subjects']) * 100
                results['backlog_count'] = len(results['backlogs'])
            
            return results if results['total_subjects'] > 0 else None
            
        except Exception as e:
            logger.error(f"Error parsing results table for {roll_number}: {str(e)}")
            return None
    
    def _extract_subject_info(self, row_data: List[str], headers: List[str]) -> Optional[Dict]:
        """
        Extract subject information from a table row
        
        Args:
            row_data: List of cell values from the row
            headers: List of column headers
            
        Returns:
            Dict containing subject information or None
        """
        try:
            subject_info = {
                'subject_name': '',
                'subject_code': '',
                'marks': '',
                'grade': '',
                'status': 'unknown',
                'semester': '',
                'credits': ''
            }
            
            # Map common column patterns
            for i, (header, data) in enumerate(zip(headers, row_data)):
                header_lower = header.lower()
                
                if 'subject' in header_lower and 'code' not in header_lower:
                    subject_info['subject_name'] = data
                elif 'code' in header_lower:
                    subject_info['subject_code'] = data
                elif 'mark' in header_lower or 'score' in header_lower:
                    subject_info['marks'] = data
                elif 'grade' in header_lower:
                    subject_info['grade'] = data
                elif 'result' in header_lower or 'status' in header_lower:
                    subject_info['status'] = data
                elif 'semester' in header_lower or 'sem' in header_lower:
                    subject_info['semester'] = data
                elif 'credit' in header_lower:
                    subject_info['credits'] = data
            
            # If no explicit status column, try to determine from marks/grade
            if subject_info['status'] == 'unknown':
                if subject_info['marks']:
                    # Try to extract numeric marks
                    marks_match = re.search(r'(\d+)', subject_info['marks'])
                    if marks_match:
                        marks = int(marks_match.group(1))
                        subject_info['status'] = 'pass' if marks >= 40 else 'fail'
                
                if subject_info['grade']:
                    grade = subject_info['grade'].upper()
                    if grade in ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'P']:
                        subject_info['status'] = 'pass'
                    elif grade in ['F', 'FAIL', 'AB', 'ABSENT']:
                        subject_info['status'] = 'fail'
            
            # Return only if we have meaningful data
            if subject_info['subject_name'] or subject_info['subject_code']:
                return subject_info
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting subject info: {str(e)}")
            return None
    
    def check_student_backlogs(self, roll_number: str, password: str = None) -> Dict:
        """
        Main method to check student backlogs
        
        Args:
            roll_number: Student roll number
            password: Student password (defaults to roll_number if not provided)
            
        Returns:
            Dict containing backlog analysis results
        """
        if not password:
            password = roll_number  # Assume roll number as password
        
        result = {
            'success': False,
            'roll_number': roll_number,
            'error': None,
            'backlog_count': 0,
            'backlogs': [],
            'total_subjects': 0,
            'passed_subjects': 0,
            'overall_status': 'unknown'
        }
        
        try:
            # Step 1: Login to SIS portal
            logger.info(f"Attempting to login for student {roll_number}")
            login_success = self.login_student(roll_number, password)
            
            if not login_success:
                result['error'] = 'Failed to login to SIS portal. Please check roll number and password.'
                return result
            
            # Step 2: Fetch and parse results
            logger.info(f"Fetching results for student {roll_number}")
            results_data = self.get_student_results(roll_number)
            
            if not results_data:
                result['error'] = 'Could not fetch results data from SIS portal.'
                return result
            
            # Step 3: Process results
            result.update({
                'success': True,
                'backlog_count': results_data.get('backlog_count', 0),
                'backlogs': results_data.get('backlogs', []),
                'total_subjects': results_data.get('total_subjects', 0),
                'passed_subjects': results_data.get('passed_subjects', 0),
                'overall_status': 'clear' if results_data.get('backlog_count', 0) == 0 else 'backlogs_present'
            })
            
            logger.info(f"Successfully processed results for {roll_number}: {result['backlog_count']} backlogs found")
            
        except Exception as e:
            logger.error(f"Unexpected error checking backlogs for {roll_number}: {str(e)}")
            result['error'] = f'Unexpected error: {str(e)}'
        
        finally:
            # Clean up session
            try:
                self.session.close()
            except:
                pass
        
        return result


# Demo/Mock implementation for testing
class MockSISIntegration:
    """Mock SIS integration for testing purposes"""
    
    def check_student_backlogs(self, roll_number: str, password: str = None) -> Dict:
        """
        Mock implementation that returns realistic demo data
        Special handling for roll number 226K1A0546
        """
        import random
        
        # Simulate some processing time
        import time
        time.sleep(1)
        
        # Special case for the specific roll number
        if roll_number == "226K1A0546":
            return {
                'success': True,
                'roll_number': roll_number,
                'error': None,
                'backlog_count': 2,
                'backlogs': [
                    {
                        'subject_name': 'Database Management Systems',
                        'subject_code': 'CS304',
                        'semester': 'Semester 5',
                        'marks': 35,
                        'grade': 'F',
                        'status': 'fail'
                    },
                    {
                        'subject_name': 'Computer Networks',
                        'subject_code': 'CS401',
                        'semester': 'Semester 6',
                        'marks': 38,
                        'grade': 'F',
                        'status': 'fail'
                    }
                ],
                'total_subjects': 42,
                'passed_subjects': 40,
                'overall_status': 'backlogs_present'
            }
        
        # Generate realistic mock data based on roll number for other students
        roll_hash = hash(roll_number) % 100
        
        if roll_hash < 70:  # 70% students have no backlogs
            return {
                'success': True,
                'roll_number': roll_number,
                'error': None,
                'backlog_count': 0,
                'backlogs': [],
                'total_subjects': random.randint(40, 50),
                'passed_subjects': random.randint(40, 50),
                'overall_status': 'clear'
            }
        else:  # 30% have backlogs
            backlog_count = random.randint(1, 5)
            backlogs = []
            
            # More realistic subject names for engineering students
            subjects = [
                'Mathematics-I', 'Mathematics-II', 'Physics', 'Chemistry', 
                'Engineering Drawing', 'Programming in C', 'Data Structures',
                'Database Management Systems', 'Computer Networks', 'Operating Systems',
                'Software Engineering', 'Web Technologies', 'Machine Learning',
                'Artificial Intelligence', 'Compiler Design', 'Computer Graphics'
            ]
            
            subject_codes = [
                'MA101', 'MA201', 'PH101', 'CH101', 'ED101', 'CS101',
                'CS201', 'CS301', 'CS401', 'CS302', 'CS402', 'CS501',
                'CS601', 'CS602', 'CS701', 'CS702'
            ]
            
            for i in range(backlog_count):
                subject_idx = random.randint(0, len(subjects) - 1)
                backlogs.append({
                    'subject_name': subjects[subject_idx],
                    'subject_code': subject_codes[subject_idx] if subject_idx < len(subject_codes) else f'CS{random.randint(100, 999)}',
                    'semester': f'Semester {random.randint(1, 8)}',
                    'marks': random.randint(20, 39),
                    'grade': 'F',
                    'status': 'fail'
                })
            
            total_subjects = random.randint(40, 50)
            return {
                'success': True,
                'roll_number': roll_number,
                'error': None,
                'backlog_count': backlog_count,
                'backlogs': backlogs,
                'total_subjects': total_subjects,
                'passed_subjects': total_subjects - backlog_count,
                'overall_status': 'backlogs_present'
            }