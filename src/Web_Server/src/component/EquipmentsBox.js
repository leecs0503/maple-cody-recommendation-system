import React, { useState } from "react";
import Base64toImg from "./Base64toImg"
import {
  Box,
} from "@mui/material";
export default function EquipmentsBox({
  thumnailImage,
  partName,
  width,
  height,
}) {
  width = typeof width === 'undefined' ? 70 : width
  height = typeof height === 'undefined' ? width : height
  let img = (
    <div />
  )
  const isThumnailImage = typeof thumnailImage !== 'undefined'
  if (isThumnailImage) {
    img = (
      <Base64toImg
        width={width - 10}
        imageData={thumnailImage}
      />
    )
  }

  return (
    <Box
      style={{
        marginBottom: 5,
        marginTop: 5,
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
      }}
      sx={{
        width: width,
        height: height,
        borderRadius: '2px',
        background: isThumnailImage ? "linear-gradient( to bottom, #998888,  #BBAAAA)" : "#BB7766",
        '&:hover': {
          backgroundColor: '#00FFFF',
          opacity: [0.9, 0.8, 0.7],
        },
      }}
    >
      <div
        style={{
          position: "relative",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: `-${height / 2 - 5}px`,
            left: `${isThumnailImage ? 0 : -width / 2 + 2}px`,
            fontSize: "7px",
            fontFamily: "inter-bold",
            color: "#CCCCCC",
            zIndex: 1
          }}
        >
          {partName}
        </div>
      </div>

      {img}
    </Box>
  )
}