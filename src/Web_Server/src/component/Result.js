import '../App.css'

import useFetch from "../hooks/useFetch";
import useInferFetch from "../hooks/useInferFetch";
import { useParams } from "react-router-dom";
import {
  Avatar,
  Typography,
} from "@mui/material";


let res_64
function Result() {
  const params = useParams();
  let id = params.id
  let character_code = useFetch("/character_code_web_handler", id);
  let infer_code = useInferFetch("/infer_code_web_handler", character_code);
  res_64 = infer_code['avatar']

  return (
    <div className="black-nav">
      <Avatar alt="Remy Sharp" src={`data:image/jpeg;base64,${res_64}`} />
      <Typography variant="h4" component="h2">
        변환 된 아바타
      </Typography>

      <Typography variant="h5" component="h2">
        캐릭터 이름 : {params.id}
      </Typography>

    </div>
  );
}
export default Result;
