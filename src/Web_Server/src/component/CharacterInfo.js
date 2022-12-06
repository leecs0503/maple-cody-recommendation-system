import React, { useState } from "react";

import {
  Grid,
  Box,
  Typography,
} from "@mui/material";
import EquipmentsGrid from "./EquipmentsGrid"
import Base64toImg from './Base64toImg'

export default function CharacterInfo({ characterInfo }) {
  if (characterInfo === null) {
    return (
      <Box
        sx={{
          p: 2, border: '1px dashed grey',
          borderRadius: '16px'
        }}
      >
        none
      </Box>
    )
  }
  return (
    <Box
      sx={{
        p: 2, border: '1px dashed grey',
        borderRadius: '16px'
      }}
    >
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <img src={characterInfo.avatar_image} />
          <Typography variant="h5">
            <Base64toImg
              imageData={characterInfo.crt_image}
            />
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <EquipmentsGrid
            characterInfo={characterInfo}
          />
        </Grid>
      </Grid>
    </Box>

  );
}
