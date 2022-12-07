import { useEffect, useState } from "react";

const TRANSFORM_STATE_TO_PARTS = [
  "hair",
  "cap",
  "face_acc",
  "eye",
  "eye_acc",
  "earrings",
  "weapon",
  "coat",
  "subweapon", 
  "pants",
  "glove",
  "cape", 
  "shoes",
]

function useRecommandFetch(cryptoUri, partState) {
  const url = 'http://localhost:7000/v1/recommend-cody'
  const parts = ["cap"]
  const [data, setData] = useState(null);
  useEffect(() => {
    if (cryptoUri === null)
      return
    if (partState === 0)
      return
    const parts = []
    
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
  }, [cryptoUri, partState]);

  return data;
}


export default useRecommandFetch;
