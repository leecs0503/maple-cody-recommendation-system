import React, { useState } from "react";
import EquipmentsBox from "./EquipmentsBox"
import {
  Grid,
} from "@mui/material";

export default function EquipmentsGrid({ characterInfo }) {
  console.log(characterInfo)
  return (
    <div>
      <Grid container spacing={2}>
        <Grid xs={3}>
          <EquipmentsBox
            thumnailImage={characterInfo.hair_thum}
          />
          <EquipmentsBox
            thumnailImage={characterInfo.eye_thum}
          />
          <EquipmentsBox
            thumnailImage={characterInfo.weapon_thum}
          />
        </Grid>
        <Grid xs={3}>

          <EquipmentsBox
            thumnailImage={characterInfo.cap_thum}
          />
          <EquipmentsBox
            thumnailImage={characterInfo.face_acc_thum}
          />
          <EquipmentsBox
            thumnailImage={characterInfo.eye_acc_thum}
          />
          <EquipmentsBox
            thumnailImage={characterInfo.long_coat_thum}
          />
          <EquipmentsBox
            thumnailImage={characterInfo.shoes_thum}
          />
        </Grid>
        <Grid xs={3}>
          <EquipmentsBox
            thumnailImage={characterInfo.earrings_thum}
          />
          <EquipmentsBox
            thumnailImage={characterInfo.glove_thum}
          />
        </Grid>
        <Grid xs={3}>
          <EquipmentsBox
            thumnailImage={characterInfo.cape_thum}
          />
        </Grid>
      </Grid>
    </div>
  )
}