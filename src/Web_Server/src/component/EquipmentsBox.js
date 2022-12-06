import React, { useState } from "react";
import Base64toImg from "./Base64toImg"
import {
  Box,
} from "@mui/material";
export default function EquipmentsBox({ thumnailImage }) {

  return (
    <Box>
      <Base64toImg
        imageData={thumnailImage}
      />
    </Box>
  )
}