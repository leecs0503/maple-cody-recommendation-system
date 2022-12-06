import { useEffect, useState } from "react";

function useRecommandFetch(cryptoUri) {
  const url = 'http://localhost:7000/v1/recommend-cody'
  const parts = ["weapon", "cape", "cap"]
  const [data, setData] = useState(null);
  useEffect(() => {
    if (cryptoUri === null)
      return
    fetch(url, {
      method: "POST",
      body: JSON.stringify({
        "crypto_uri": cryptoUri,
        "parts": parts
      })
    })
      .then(res => {
        return res.json();
      })
      .then(data => {
        setData(data);
      });
  }, [cryptoUri]);

  return data;
}


export default useRecommandFetch;
