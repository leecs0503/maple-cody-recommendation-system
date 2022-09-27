from src.ImageServer.Avatar.avatar import Avatar


def test_avartar():
    avatar = Avatar(
        face="1",
        hair="2",
        longcoat="3",
        weapon="4",
    )

    assert avatar.to_array() == ["1", "2", "3", "4"]
    assert avatar.to_param() == [("Face", "1"), ("Hair", "2"), ("Longcoat", "3"), ("Weapon", "4")]
