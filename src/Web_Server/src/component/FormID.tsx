import React, { useEffect, useState } from "react";
import useFetch from "../hooks/useFetch";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {
  Grid,
  Button,
  FormGroup,
  TextField,
} from "@mui/material";

const theme = createTheme({
  palette: {
    neutral: {
      main: '#e53e3e',
      contrastText: '#FFFFFF',
    },
  },
});



export default function FormID({ setCharacterInfo }) {
  const [textFieldUserName, setTextFieldUserName] = useState("");
  const [userId, setUserId] = useState(null);
  const handleTextFieldChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setTextFieldUserName(event.target.value)
  };
  const characterInfo = useFetch("http://localhost:7000/v1/character-info", userId);
  const characterImageSubmit = () => {
    setUserId(textFieldUserName)
  }
  useEffect(() => {
    setCharacterInfo(characterInfo)
  }, [characterInfo]);

  return (
    <FormGroup
      sx={{
        padding: 2,
        borderRadius: 2,
        border: "1px solid",
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
        <Button color="neutral" variant="outlined" component="label" size="large" onClick={characterImageSubmit}>Submit</Button>
      </ThemeProvider>
    </FormGroup>

  );
}
