import React, { Fragment, useState } from "react";
import useFetch from "../hooks/useFetch";
import CharacterInfo from "./CharacterInfo";
import InferImage from "./InferImage";
import MainIntro from "./MainIntro"
import { createTheme,ThemeProvider } from '@mui/material/styles';
import {
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
          <FormGroup
            sx={{
              padding: 2,
              borderRadius: 2,
              border: "1px solid",
              borderColor: "error.main",
            }}
          >
            <TextField
              sx={{ paddingBottom: 2 }}
              name="UserID"
              variant="outlined"
              placeholder="UserId를 입력하세요"
              onChange={handleTextFieldChange}
            />
          <ThemeProvider theme={theme}>
            <Button color="neutral" variant="contained" component="label"  size="large" onClick={characterImageSubmit}>Submit</Button>
          </ThemeProvider>
          </FormGroup>

        </Grid>
        <Grid item xs={2}>
          <InferImage image_name={[1,4]} code={character_code}/>
        </Grid>
        <Grid item xs={2}>
          <InferImage image_name={[2,5]} code={character_code}/>
        </Grid>
        <Grid item xs={2}>
          <InferImage image_name={[3,6]} code={character_code}/>
        </Grid>
      </Grid>
    </Fragment>

  );
}
