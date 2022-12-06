import React, { useState } from "react";
import EquipmentsBox from "./EquipmentsBox"
import {
  Grid,
} from "@mui/material";

export default function EquipmentsGrid({ characterInfo }) {
  console.log(characterInfo)
  const girdStyle = {
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
  }
  return (
    <div
      style={{
        marginTop: "16px"
      }}
    >
      <Grid container spacing={2}>
        {/* row 1 */}
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="HAIR"
            width={70}
            height={150}
            thumnailImage={characterInfo.hair_thum}
          />
        </Grid>
        <Grid xs={3} style={{
          ...girdStyle,
          flexDirection: "column"
        }}>
          <EquipmentsBox
            partName="CAP"
            thumnailImage={characterInfo.cap_thum}
          />
          <EquipmentsBox
            partName="FACE ACC"
            thumnailImage={characterInfo.face_acc_thum}
          />
        </Grid>
        <Grid xs={6}>
        </Grid>
        {/* row 2 */}
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="EYE"
            thumnailImage={characterInfo.eye_thum}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="EYE ACC"
            thumnailImage={characterInfo.eye_acc_thum}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            thumnailImage={characterInfo.earrings_thum}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
        </Grid>
        {/* row 3 */}
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="WEAPON"
            thumnailImage={characterInfo.weapon_thum}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="COAT"
            thumnailImage={characterInfo.long_coat_thum}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="SUBWEAPON"
          />
        </Grid>
        {/* row 4 */}
        <Grid xs={3} style={girdStyle}>
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="PANTS" />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="GLOVE"
            thumnailImage={characterInfo.glove_thum}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="CAPE"
            thumnailImage={characterInfo.cape_thum}
          />
        </Grid>
        {/* row 5 */}
        <Grid xs={3} style={girdStyle}>
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="SHOES"
            thumnailImage={characterInfo.shoes_thum}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
        </Grid>
        <Grid xs={3} style={girdStyle}>
        </Grid>
      </Grid>
    </div>
  )
}