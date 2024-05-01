import React, {createContext} from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import Store from "./storage/store";

const store = new Store()

export const Context = createContext({
  store
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Context.Provider value={{store}}>
    <React.StrictMode>
      <App/>
    </React.StrictMode>
  </Context.Provider>
);
