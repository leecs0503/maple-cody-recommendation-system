import React, { useState } from "react";
import Base64toImg from "./Base64toImg"
import {
  Box,
  Tooltip,
} from "@mui/material";
export default function EquipmentsBox({
  thumnailImage,
  nameImage,
  partName,
  partIndex,
  partStateToRecommand,
  setPartStateToRecommand,
  width,
  height,
}) {
  width = typeof width === 'undefined' ? 70 : width
  height = typeof height === 'undefined' ? width : height
  let img = (
    <div />
  )
  const isThumnailImage = typeof thumnailImage !== 'undefined'
  const isPartStateToRecommand = typeof partStateToRecommand !== 'undefined' 
  const onClickBox = (event) => {
    if (!isPartStateToRecommand) {
      return
    }
    setPartStateToRecommand(partStateToRecommand ^ (1 << partIndex))
  }
  if (isThumnailImage) {
    img = (
      <Base64toImg
        width={width - 10}
        imageData={thumnailImage}
      />
    )
  }
  const opacityState = {}
  if (isPartStateToRecommand && ((partStateToRecommand & (1 << partIndex)) > 0)) {
    console.log(partStateToRecommand, (1 << partIndex), partIndex)
    opacityState["opacity"] = [0.8,0.7,0.6]
  }


  return (
    <Tooltip title={nameImage} placement="right-start">
      <Box
        onClick={onClickBox}
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
            opacity: [0.9, 0.8, 0.7],
          },
          ...opacityState
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
    </Tooltip>
  )
}