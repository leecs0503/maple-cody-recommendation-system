import React, { useState } from "react";
import {
  Grid,
  Box,
  Divider,
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
        유저 아이디를 입력해주세요
      </Box>
    )
  }
  return (
    <Box
      sx={{
        p: 2,
        border: '1px dashed grey',
        borderRadius: '16px',
      }}
    >
      <Grid container spacing={2}>
        <Grid item xs={5}
          style={{
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            flexDirection: "column"
          }}>
          <Base64toImg
            width={144}
            height={144}
            imageData={characterInfo.crt_image}
          />
          <br />
          <Box
            sx={{
              // backgroundColor: "black",
              // color: "white",
              borderRadius: '3px',
              marginTop: "-20px",
            }}
          >
            {characterInfo.user_name}
          </Box>

        </Grid>
        <Divider orientation="vertical" flexItem style={{ marginTop: "16px" }} />

        <Grid item xs={1}></Grid>
        <Grid item xs={5}>
          <EquipmentsGrid
            characterInfo={characterInfo}
          />
        </Grid>
      </Grid>
    </Box>

  );
}
