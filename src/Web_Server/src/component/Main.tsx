import React, { useState } from "react";

import {
  Button,
  FormGroup,
  TextField,
} from "@mui/material";

import { useNavigate } from 'react-router';

interface FormValues {
  specs?: string;
}

export default function Main() {
  const navigate = useNavigate();
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

  const handleSubmit = () => {
    let id = formValues.UserID
    navigate(`/${id}`);
  }

  return (
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
  );
}
