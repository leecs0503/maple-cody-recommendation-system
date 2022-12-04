import React, { useState } from "react";
import useFetch from "../hooks/useFetch";

import {
  Box,
  Card,
  Typography,
  CardContent,
  Paper,
  Grid,
  Button,
  FormGroup,
  TextField,
} from "@mui/material";
interface FormValues {
  specs?: string;
}

export default function Main() {
  const [formValues, setFormValues] = useState<FormValues>({});

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

  const handleSubmit = () => {
    console.log(character_code.avatar_image)

  }

  return (
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            '& > :not(style)': {
              m: 1,
              width: 1250,
              height: 450,
            },
          }}
        >
          <Paper elevation={3} >
          <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            '& > :not(style)': {
              m: 1,
              width: 150,
              height: 50,
            },
          }}
        >
        <Paper elevation={3} >
        </Paper>
        <Paper elevation={3} >
        </Paper>
        <Paper elevation={3} >
        </Paper>
        <Paper elevation={3} >
        </Paper>
        </Box>

        <Card sx={{ minWidth: 275 }}>
          <CardContent>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              <br />
              <img src = {character_code.avatar_image}/>
              <br />
              <br />
            </Typography>
            <Typography variant="h5">
              캐릭터 이미지
              <br />
              <br />
              <Button variant="outlined" >추론하기</Button>
            </Typography>
          </CardContent>
        </Card>

        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            '& > :not(style)': {
              m: 1,
              width: 150,
              height: 50,
            },
          }}
        >
        <Paper elevation={3} >
        </Paper>
        <Paper elevation={3} >
        </Paper>
        <Paper elevation={3} >
        </Paper>
        <Paper elevation={3} >
        </Paper>
        </Box>
        </Paper>
        </Box>
        <br />
        <FormGroup
          sx={{
            padding: 2,
            borderRadius: 2,
            border: "1px solid",
            borderColor: "primary.main",
          }}
        >
          <TextField
            sx={{ paddingBottom: 2 }}
            name="UserID"
            variant="outlined"
            placeholder="UserId를 입력하세요"
            onChange={handleTextFieldChange}
          />
          <Button variant="outlined" onClick={handleSubmit}>Submit</Button>
        </FormGroup>
      </Grid>

      <Grid item xs={2}>
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            '& > :not(style)': {
              m: 1,
              width: 1250,
              height: 300,
            },
          }}
        >
          <Paper elevation={3}>
          </Paper>
          <Paper elevation={3}>
          </Paper>
        </Box>
      </Grid>

      <Grid item xs={2}>
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            '& > :not(style)': {
              m: 1,
              width: 1250,
              height: 300,
            },
          }}
        >
          <Paper elevation={3}>
          </Paper>
          <Paper elevation={3}>
          </Paper>
        </Box>
      </Grid>

      <Grid item xs={2}>
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            '& > :not(style)': {
              m: 1,
              width: 1250,
              height: 300,
            },
          }}
        >
          <Paper elevation={3}>
          </Paper>
          <Paper elevation={3}>
          </Paper>
        </Box>
      </Grid>
    </Grid>
  );
}
