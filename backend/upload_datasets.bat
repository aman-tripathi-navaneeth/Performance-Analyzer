@echo off
echo Uploading 4th Year CSE A Datasets...
echo =====================================

curl -X POST -F "file=@sample_data/cs401_machine_learning_4th_year_cse_a.csv" http://localhost:5000/api/v1/uploads/upload
echo.

curl -X POST -F "file=@sample_data/cs402_software_engineering_4th_year_cse_a.csv" http://localhost:5000/api/v1/uploads/upload
echo.

curl -X POST -F "file=@sample_data/cs403_computer_networks_4th_year_cse_a.csv" http://localhost:5000/api/v1/uploads/upload
echo.

curl -X POST -F "file=@sample_data/cs404_database_management_systems_4th_year_cse_a.csv" http://localhost:5000/api/v1/uploads/upload
echo.

curl -X POST -F "file=@sample_data/cs405_artificial_intelligence_4th_year_cse_a.csv" http://localhost:5000/api/v1/uploads/upload
echo.

curl -X POST -F "file=@sample_data/cs406_compiler_design_4th_year_cse_a.csv" http://localhost:5000/api/v1/uploads/upload
echo.

echo =====================================
echo Upload complete!
pause