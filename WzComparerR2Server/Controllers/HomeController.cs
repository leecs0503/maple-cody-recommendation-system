using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using WzComparerR2Server.Models;
using WzComparerR2.Avatar;
using MainProgram;

namespace WzComparerR2Server.Controllers;

public class HomeController : Controller
{

    AvatarCanvas avatar;

    public string Index() // TODO : ActionResult
    {
        var dir = Directory.GetCurrentDirectory();
        var path = Path.Combine(dir, "a.png");
        var imageFileStream = System.IO.File.OpenRead(path);
        return Program.wz.WzNode.nodes[0].text;
        // return base.File(imageFileStream,"image/png");
    }

    // private bool AvatarInit()
    //     {
    //         this.inited = this.avatar.LoadZ()
    //             && this.avatar.LoadActions()
    //             && this.avatar.LoadEmotions();

    //         if (this.inited)
    //         {
    //             this.FillBodyAction();
    //             this.FillEmotion();
    //         }
    //         return this.inited;
    //     }
}
