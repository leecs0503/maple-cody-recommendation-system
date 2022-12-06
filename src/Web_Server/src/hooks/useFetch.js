import { useEffect, useState } from "react";

function useFetch(url, userid) {
  const [data, setData] = useState(null);
  useEffect(() => {
    if (userid === null)
      return
    fetch(url, {
      method: "POST",
      body: JSON.stringify({ "user_name": userid })
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
