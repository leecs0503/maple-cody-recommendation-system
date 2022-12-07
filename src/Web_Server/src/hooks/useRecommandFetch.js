import { useEffect, useState } from "react";

const TRANSFORM_STATE_TO_PARTS = [
  "hair",
  "cap",
  "faceAccessory",
  "face",
  "eyeAccessory",
  "earrings",
  "weapon",
  "longcoat",
  "glove",
  "cape", 
  "shoes",
]

function useRecommandFetch(cryptoUri, partState) {
  const url = 'http://vqateam12.kro.kr:8383/v1/recommend-cody'
  const [data, setData] = useState(null);
  useEffect(() => {
    if (cryptoUri === null)
      return
    if (partState === 0)
      return
    const parts = []
    for (const idx in TRANSFORM_STATE_TO_PARTS) {
      if (partState & (1 << idx)) {
        parts.push(TRANSFORM_STATE_TO_PARTS[idx])
      }
    }
    
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
