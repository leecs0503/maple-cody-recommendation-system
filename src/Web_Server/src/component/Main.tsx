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
} from "@mui/material";
import InferResultBox from './InferResultBox'

export default function Main() {
  const [characterInfo, setCharacterInfo] = useState(null);
  const [recommandInfo, setRecommandInfo] = useState({
    "cryptoUriToRecommand": null,
    "partStateToRecommand": 0,
  });
  const [partStateToRecommand, setPartStateToRecommand] = useState(0);
  const recommandedInfo = useRecommandFetch(recommandInfo.cryptoUriToRecommand, recommandInfo.partStateToRecommand);
  const onRecommandButtonClick = (event) => {
    if (characterInfo === null) {
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
      <MainIntro />
      <Grid container spacing={2}>
        <Grid item xs={0.5}>
        </Grid>
        <Grid item xs={5}>
          <CharacterInfo
            characterInfo={characterInfo}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
          />
          <br />
          <FormID setCharacterInfo={setCharacterInfo} setCryptoUriToRecommand={setCryptoUriToRecommand}/>
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
        {/* <Grid item xs={2}>
          <Box
            sx={{
              p: 2, border: '1px dashed grey',
              borderRadius: '16px'
            }}
          >
            <InferImage image_name={[1, 4]} code={character_code} />
          </Box>
        </Grid>
        <Grid item xs={2}>
          <Box
            sx={{
              p: 2, border: '1px dashed grey',
              borderRadius: '16px'
            }}
          >
            <InferImage image_name={[2, 5]} code={character_code} />
          </Box>
        </Grid>
        <Grid item xs={2}>
          <Box
            sx={{
              p: 2, border: '1px dashed grey',
              borderRadius: '16px'
            }}
          >
            <InferImage image_name={[3, 6]} code={character_code} />
          </Box>
        </Grid> */}
      </Grid>
    </Fragment>

  );
}
