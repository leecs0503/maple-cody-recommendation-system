import { useEffect, useState } from "react";
function useInferFetch(url, code) {
  const [data, setData] = useState([]);
  useEffect(() => {
    fetch(url, {
        method : "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body : JSON.stringify({'character_code_result':code})
    })
      .then(res => {
        return res.json();
      })
      .then(data => {
        setData(data);
      });
  }, [url, code]);

  return data;
}

export default useInferFetch;
