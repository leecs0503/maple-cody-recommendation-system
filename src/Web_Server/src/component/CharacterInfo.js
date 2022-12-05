import React, { useState } from "react";

import {
    Grid,
    Box,
    Card,
    Typography,
    CardContent,
    Paper,
    Button,
  } from "@mui/material";
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

export default function CharacterInfo(props) {

    const [devices, setDevices] = React.useState(() => []);
    let character_code = props.code
    console.log(character_code)
    const handleDevices = (
        event: React.MouseEvent<HTMLElement>,
        newDevices: string[],
    ) => {
        if (newDevices.length) {
        setDevices(newDevices);
        }
    };

  const inferSubmit = () => {
    //devices에 토클에 선택된 것들이 배열형태로 저장
    //예를 들어 무기랑 모자 선택하면 ['weapon','hat']
      console.log(devices);
    }

  return (
    <Grid container spacing={2}>
      <Grid item xs={2}>
      <br/>
      <Paper elevation={1} >
      <br/>
      헤어
      <br/>
      <br/>
      </Paper>
      <br/>
      <br/>
      <br/>
      <Paper elevation={1} >
      <br/>
      눈
      <br/>
      <br/>
      </Paper>
      <br/>
      <br/>
      <br/>
      <Paper elevation={1} >
      <br/>
      얼장
      <br/>
      <br/>
      </Paper>
      <br/>
      <br/>
      <br/>
      <Paper elevation={1} >
      <br/>
      눈장
      <br/>
      <br/>
      </Paper>
      </Grid>

      <Grid item xs={8}>
    <Typography sx={{ mb: 1.5 }} color="text.secondary">
        <img src = {character_code.avatar_image}/>
    </Typography>
      <br/>
      <br/>
      <br/>
      <br/>
      <br/>
      <br/>

    <Typography variant="h5">
        캐릭터 이미지
        <ToggleButtonGroup
    value={devices}
    onChange={handleDevices}
    aria-label="device"
    >
    <ToggleButton value="hair" aria-label="hair">
    헤어
    </ToggleButton>
    <ToggleButton value="hat" aria-label="hat">
    모자
    </ToggleButton>
    <ToggleButton value="cloth" aria-label="cloth">
    단벌옷
    </ToggleButton>
    <ToggleButton value="weapon" aria-label="weapon">
    무기
    </ToggleButton>
    <ToggleButton value="faceAccessory" aria-label="faceAccessory">
    얼장
    </ToggleButton>
    <ToggleButton value="eyeAccessory" aria-label="eyeAccessory">
    눈장
    </ToggleButton>
    <ToggleButton value="eye" aria-label="eye">
    눈
    </ToggleButton>
    <ToggleButton value="cape" aria-label="cape">
    망토
    </ToggleButton>
    </ToggleButtonGroup>
    <br />
    <br />

    <Button variant="outlined" onClick={inferSubmit}>추론하기</Button>
    </Typography>

      </Grid>
      <Grid item xs={2}>
      <br/>
      <Paper elevation={1} >
      <br/>
      모자
      <br/>
      <br/>
      </Paper>
      <br/>
      <br/>
      <br/>
      <Paper elevation={1} >
      <br/>
      단벌 옷
      <br/>
      <br/>
      </Paper>
      <br/>
      <br/>
      <br/>
      <Paper elevation={1} >
      <br/>
      무기
      <br/>
      <br/>
      </Paper>
      <br/>
      <br/>
      <br/>
      <Paper elevation={1} >
      <br/>
      망토
      <br/>
      <br/>
      </Paper>
      <br/>
      </Grid>
    </Grid>
  );
}
