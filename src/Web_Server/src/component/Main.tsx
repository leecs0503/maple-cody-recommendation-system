import React, { Fragment, useState } from "react";
import useFetch from "../hooks/useFetch";
import useRecommandFetch from "../hooks/useRecommandFetch";
import CharacterInfo from "./CharacterInfo";
import FormID from "./FormID.tsx";
import InferImage from "./InferImage";
import MainIntro from "./MainIntro"
import { createTheme, ThemeProvider } from '@mui/material/styles';
import SendIcon from '@mui/icons-material/Send';
import {
  Grid,
  Button,
  Snackbar,
  Alert,
} from "@mui/material";
import InferResultBox from './InferResultBox'

export default function Main() {
  const [characterInfo, setCharacterInfo] = useState(null);
  const [recommandInfo, setRecommandInfo] = useState({
    "cryptoUriToRecommand": null,
    "partStateToRecommand": 0,
  });
  const [snackBar1Open, setSnackBar1Open] = useState(false)
  const [snackBar2Open, setSnackBar2Open] = useState(false)
  const [partStateToRecommand, setPartStateToRecommand] = useState(0);
  const recommandedInfo = useRecommandFetch(recommandInfo.cryptoUriToRecommand, recommandInfo.partStateToRecommand);

  const snackBar1HandleClose = (event, reason)=>{
    if (reason === 'clickaway') {
      return;
    }
    setSnackBar1Open(false)
  }
  const snackBar2HandleClose = (event, reason)=>{
    if (reason === 'clickaway') {
      return;
    }
    setSnackBar2Open(false)
  }

  const onRecommandButtonClick = (event) => {
    if (characterInfo === null) {
      setSnackBar1Open(true)
      return
    }
    if (partStateToRecommand === 0) {
      setSnackBar2Open(true)
      return
    }
    setRecommandInfo({
      cryptoUriToRecommand: characterInfo.crypto_uri,
      partStateToRecommand,
    });
  }
  console.log(recommandedInfo)
  return (
    <Fragment>
      <Snackbar open={snackBar1Open} autoHideDuration={6000} onClose={snackBar1HandleClose}>
        <Alert onClose={snackBar1HandleClose} severity="info" sx={{ width: '100%' }}>
          유저 아이디를 먼저 입력하세요
        </Alert>
      </Snackbar>
      <Snackbar open={snackBar2Open} autoHideDuration={6000} onClose={snackBar2HandleClose}>
        <Alert onClose={snackBar2HandleClose} severity="info" sx={{ width: '100%' }}>
          아무 장비도 선택하지 않았습니다. <br/>
          변환하고 싶은 장비 아이템을 클릭해서 추천 여부를 토글링 할 수 있습니다.
        </Alert>
      </Snackbar>
      <MainIntro />
      <Grid container spacing={2}>
        <Grid item xs={0.25}>
        </Grid>
        <Grid item xs={5}>
          <CharacterInfo
            characterInfo={characterInfo}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
          />
          <br />
          <FormID setCharacterInfo={setCharacterInfo} setRecommandInfo={setRecommandInfo}/>
        </Grid>
        <Grid item xs={1} style={{
          "display": "flex",
          "alignItems": "center",
          "justifyContent": "center",
        }}>
          <Button variant="contained" endIcon={<SendIcon />} color="error" onClick={onRecommandButtonClick}>
            추천
          </Button>
        </Grid>

        <Grid item xs={5.5}>
          <InferResultBox
            recommandedInfo = {recommandedInfo}
          />
        </Grid>
      </Grid>
      <div style={{height: "10vh"}}>

      </div>
    </Fragment>

  );
}
