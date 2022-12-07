import React, { useState } from "react";
import {
  Box,
  Grid,
  Divider,
} from "@mui/material";
import Base64toImg from "./Base64toImg";
import EquipmentsGrid from "./EquipmentsGrid";

export default function InferResultBox({ recommandedInfo }) {
  if (recommandedInfo === null) {
    return (
      <Box
        sx={{
          p: 2, border: '1px dashed grey',
          borderRadius: '16px'
        }}
      >
        추천 전입니다.
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
              imageData={recommandedInfo["recommended image"]}
          />
        </Grid>
        <Divider orientation="vertical" flexItem style={{ marginTop: "16px" }} />
        <Grid item xs={1}></Grid>
        <Grid item xs={5}>
          <EquipmentsGrid
            characterInfo={recommandedInfo.result_parts}
          />
        </Grid>
      </Grid>
    </Box>

  );
}
