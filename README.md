# maple-cody-recommandation-system
22-2R 캡스톤디자인 AI 메이플 코디 추천 시스템



pyrightconfig.json
{
  "include": ["."],
  "exclude": [
    ".venv",
    "docker",
    "pb1",
    "pb2",
    "pb3",
    "pb_meta",
    "test-*.py",
    ".downloaded-modules",
    ".data"
  ],

  "stubPath": "./typings",

  "reportTypeshedErrors": true,
  "reportMissingImports": false,

  "pythonVersion": "3.8",
  "pythonPlatform": "Windows"
}
run-check.sh
#!/bin/bash

set -eux

echo "check with flake8"
python -m flake8

echo "check with isort"
isort -c .

echo "check with pyright"
pyright -p `dirname "$0"` .