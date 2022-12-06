import React, { Fragment, useState } from "react";
import useFetch from "../hooks/useFetch";
import CharacterInfo from "./CharacterInfo";
import FormID from "./FormID.tsx";
import InferImage from "./InferImage";
import MainIntro from "./MainIntro"
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {
  Box,
  Grid,
  Button,
  FormGroup,
  TextField,
} from "@mui/material";


export default function Main() {
  const [characterInfo, setCharacterInfo] = useState(null)
  console.log(characterInfo)

  return (
    <Fragment>
      <MainIntro />
      <Grid container spacing={2}>
        <Grid item xs={0.5}>
        </Grid>
        <Grid item xs={5}>
          <CharacterInfo characterInfo={characterInfo} />
          <br />
          <FormID setCharacterInfo={setCharacterInfo} />
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
