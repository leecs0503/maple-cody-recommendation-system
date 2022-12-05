import React, { useState } from "react";
import useFetch from "../hooks/useFetch";
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



export default function FormID() {
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

  );
}
