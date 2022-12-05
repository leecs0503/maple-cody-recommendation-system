import React, { Fragment, useState } from "react";
import useFetch from "../hooks/useFetch";
import CharacterInfo from "./CharacterInfo";
import FormID from "./FormID.tsx";
import InferImage from "./InferImage";
import MainIntro from "./MainIntro"
import { createTheme,ThemeProvider } from '@mui/material/styles';
import {
  Box,
  Grid,
  Button,
  FormGroup,
  TextField,
} from "@mui/material";

interface FormValues {
  specs?: string;
}


const theme = createTheme({
  palette: {
    neutral: {
      main: '#e53e3e',
      contrastText: '#FFFFFF',
    },
  },
});


export default function Main() {
  const [formValues, setFormValues] = useState<FormValues>({});
  const [devices, setDevices] = useState(() => []);

  const handleTextFieldChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;

    setFormValues({
      ...formValues,
      [name]: value,
    });
  };

  let character_code = useFetch("/character_code_web_handler", formValues.UserID);
  // 추론 관련 API 업데이트 하면 받아 오는 코드
  // let infer_image = useFetch("/character_code_web_handler", devices);

  const characterImageSubmit = () => {
    console.log(character_code.avatar_image)
  }
  return (
    <Fragment>
      <MainIntro/>
      <Grid container spacing={2}>
      <Grid item xs={0.5}>
      </Grid>
        <Grid item xs={5}>
          <CharacterInfo code={character_code} device={devices} />
          <br/>
          <FormID />
        </Grid>

        <Grid item xs={2}>
        <Box
      sx={{
        p: 2, border: '1px dashed grey',
        borderRadius: '16px'
      }}
    >
          <InferImage image_name={[1,4]} code={character_code}/>
      </Box>
        </Grid>
        <Grid item xs={2}>
        <Box
      sx={{
        p: 2, border: '1px dashed grey',
        borderRadius: '16px'
      }}
    >
          <InferImage image_name={[2,5]} code={character_code}/>
      </Box>
        </Grid>
        <Grid item xs={2}>
        <Box
      sx={{
        p: 2, border: '1px dashed grey',
        borderRadius: '16px'
      }}
    >
          <InferImage image_name={[3,6]} code={character_code}/>
      </Box>
        </Grid>
      </Grid>
    </Fragment>

  );
}
