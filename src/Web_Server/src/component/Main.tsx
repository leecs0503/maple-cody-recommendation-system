import React, { useState } from "react";
import useFetch from "../hooks/useFetch";
import CharacterInfo from "./CharacterInfo";
import InferImage from "./InferImage";
import {
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
  const [devices, setDevices] = React.useState(() => []);

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
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <CharacterInfo code={character_code} device={devices} />
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
          <Button variant="outlined" onClick={characterImageSubmit}>Submit</Button>
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
  );
}
