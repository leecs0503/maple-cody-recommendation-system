using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using WzComparerR2Server.Models;

namespace WzComparerR2Server.Controllers;

public class HomeController : Controller
{
    public ActionResult Index()
    {
        var dir = Directory.GetCurrentDirectory();
        var path = Path.Combine(dir, "a.png");
        var imageFileStream = System.IO.File.OpenRead(path);
        return base.File(imageFileStream,"image/png");
    }
}
