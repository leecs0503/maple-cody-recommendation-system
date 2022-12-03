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

export default function FormSubmitHooks() {
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
    let id = formValues.specs
    navigate(`/${id}`);
    console.log(formValues);
  }

  return (
    <form>
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
          name="specs"
          variant="outlined"
          placeholder="Specs..."
          onChange={handleTextFieldChange}
        />
        <Button variant="outlined" onClick={handleSubmit}>Submit</Button>
      </FormGroup>
    </form>
  );
}
