declare module 'react' {
  const React: any;
  export = React;
  export as namespace React;
}

declare module 'react-dom' {
  const ReactDOM: any;
  export = ReactDOM;
  export as namespace ReactDOM;
}

declare module 'react-router-dom' {
  export const useNavigate: any;
  export const useLocation: any;
  export const useParams: any;
  export const BrowserRouter: any;
  export const Routes: any;
  export const Route: any;
}