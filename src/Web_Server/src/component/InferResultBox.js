import React, { useState } from "react";
import {
  Box,
} from "@mui/material";
import Base64toImg from "./Base64toImg";

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
        <Base64toImg
            width={144}
            imageData={recommandedInfo["recommended image"]}
        />
    </Box>

  );
}
