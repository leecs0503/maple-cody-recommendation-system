import React, { useState } from "react";

import {
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
    <Box
    sx={{
    display: 'flex',
    flexWrap: 'wrap',
    '& > :not(style)': {
        m: 1,
        width: 1250,
        height: 455,
    },
    }}
    >
    <Paper elevation={1} >
    <Box
    sx={{
    display: 'flex',
    flexWrap: 'wrap',
    '& > :not(style)': {
        m: 1,
        width: 125,
        height: 50,
    },
    }}
    >
    <Paper elevation={1} >
    헤어
    </Paper>

    <Paper elevation={1} >
    모자
    </Paper>
    <Paper elevation={1} >
    단벌 옷
    </Paper>
    <Paper elevation={1} >
    무기
    </Paper>
    </Box>
    <Box
    sx={{
    display: 'flex',
    flexWrap: 'wrap',
    '& > :not(style)': {
        m: 1,
        width: 525,
        height: 115,
    },
    }}
    >
    <Typography sx={{ mb: 1.5 }} color="text.secondary">
        <img src = {character_code.avatar_image}/>
        <br />
        <br />
    </Typography>
    <Typography variant="h5">
        캐릭터 이미지
        <br />
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
    </Box>

    <br />
    <br />

    <Box
    sx={{
    display: 'flex',
    flexWrap: 'wrap',
    '& > :not(style)': {
        m: 1,
        width: 125,
        height: 50,
    },
    }}
    >
    <Paper elevation={1} >
    얼장
    </Paper>
    <Paper elevation={1} >
    눈장
    </Paper>
    <Paper elevation={1} >
    눈
    </Paper>
    <Paper elevation={1} >
    망토
    </Paper>
    </Box>
    </Paper>

    </Box>
  );
}
