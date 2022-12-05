import './MainIntro.css';
import Grid from '@mui/material/Grid';
import { Typography, Box } from '@mui/material';
import { Fragment } from "react";
export default function MainIntro() {
  return (
    <Fragment>
      <Box style={{
        "width": "70vw",
        "paddingTop": "7.5vh",
      }}>
        <div className="top-nav" style={{
          "display": "flex",
          "alignItems": "center",
          "justifyContent": "center",
        }}>
          <Typography
            variant="h3"
            fontFamily="inter-extra-bold"
            color="#e53e3e"
          >
            Maplestory&nbsp;
          </Typography>
          <Typography
            variant="h3"
            fontFamily="inter-extra-bold"
          >
            Cody Recommand Site
          </Typography>
        </div>
        <div className="top-nav" style={{
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        }}>
          재의의 요구가 있을 때에는 국회는 재의에 붙이고, 재적의원과반수의 출석과 출석의원 3분의 2 이상의 찬성으로 전과 같은 의결을 하면 그 법률안은 법률로서 확정된다.
          <br/>
          누구든지 체포 또는 구속의 이유와 변호인의 조력을 받을 권리가 있음을 고지받지 아니하고는 체포 또는 구속을 당하지 아니한다. 체포 또는 구속을 당한 자의 가족등 법률이 정하는 자에게는 그 이유와 일시·장소가 지체없이 통지되어야 한다.
        </div>
        <div className="top-nav" style={{
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        }}>
          git 버튼
          뭐시기버튼
        </div>
      </Box>
    </Fragment>
  );
}
