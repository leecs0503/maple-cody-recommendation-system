import { useEffect, useState } from "react";

function useFetch(url, userid) {
  const [data, setData] = useState([]);
  useEffect(() => {
    fetch(url, {
        method : "POST",
        body : JSON.stringify({name: userid})
    })
      .then(res => {
        return res.json();
      })
      .then(data => {
        setData(data);
      });
  }, [url, userid]);

  return data;
}


export default useFetch;
