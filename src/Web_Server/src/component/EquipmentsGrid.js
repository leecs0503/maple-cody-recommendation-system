import React, { useState } from "react";
import EquipmentsBox from "./EquipmentsBox"
import {
  Grid,
} from "@mui/material";

export default function EquipmentsGrid({
  characterInfo,
  partStateToRecommand,
  setPartStateToRecommand,
}) {
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
            partsIndex={0}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.hair_thum}
            nameImage={characterInfo.hair_name}
          />
        </Grid>
        <Grid xs={3} style={{
          ...girdStyle,
          flexDirection: "column"
        }}>
          <EquipmentsBox
            partName="CAP"
            partsIndex={1}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.cap_thum}
            nameImage={characterInfo.cap_name}
          />
          <EquipmentsBox
            partName="FACE ACC"
            partsIndex={2}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.face_acc_thum}
            nameImage={characterInfo.face_acc_name}
          />
        </Grid>
        <Grid xs={6}>
        </Grid>
        {/* row 2 */}
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="EYE"
            partsIndex={3}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.eye_thum}
            nameImage={characterInfo.eye_name}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="EYE ACC"
            partsIndex={4}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.eye_acc_thum}
            nameImage={characterInfo.eye_acc_name}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="EAR RING"
            partsIndex={5}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.earrings_thum}
            nameImage={characterInfo.earrings_name}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
        </Grid>
        {/* row 3 */}
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="WEAPON"
            partsIndex={6}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.weapon_thum}
            nameImage={characterInfo.weapon_name}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="COAT"
            partsIndex={7}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.long_coat_thum}
            nameImage={characterInfo.long_coat_name}
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
            partsIndex={8}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.glove_thum}
            nameImage={characterInfo.glove_name}
          />
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="CAPE"
            partsIndex={9}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.cape_thum}
            nameImage={characterInfo.cape_name}
          />
        </Grid>
        {/* row 5 */}
        <Grid xs={3} style={girdStyle}>
        </Grid>
        <Grid xs={3} style={girdStyle}>
          <EquipmentsBox
            partName="SHOES"
            partsIndex={10}
            partStateToRecommand={partStateToRecommand}
            setPartStateToRecommand={setPartStateToRecommand}
            thumnailImage={characterInfo.shoes_thum}
            nameImage={characterInfo.shoes_name}
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