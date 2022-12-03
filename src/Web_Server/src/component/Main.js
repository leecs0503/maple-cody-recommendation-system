import { useNavigate } from "react-router-dom";
import {useRef} from 'react';
import '../App.css'

export default function Main() {
  let navigate = useNavigate();

  function onSubmit(e) {
    e.preventDefault();
    const id = idRef.current.value;
    navigate(`/result/${id}`);
  }

    const idRef = useRef(null);

    return (
    <div className="black-nav">
    <h2>maple cody recommendation system</h2>
    <form onSubmit={onSubmit}>
      <input id= 'input1' type="text" placeholder="ID를 입력 하세요" ref={idRef} />
      <button id='input2' type='submit'> 검색 </button>
    </form>
  </div>
);
}