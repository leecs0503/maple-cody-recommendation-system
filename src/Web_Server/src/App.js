
import React from "react";
import Header from "./component/Header";
import Main from "./component/Main";
import Result from "./component/Result";

import { Route, Routes } from "react-router-dom";
function App() {
  return (
      <div className="App">
        <Header />
        <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/result/:id" element={<Result />} />
        </Routes>
      </div>
  );
}
export default App;