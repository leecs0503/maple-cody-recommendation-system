using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using WzComparerR2Server.Models;
using WzComparerR2.Avatar;
using WzComparerR2.WzLib;
using MainProgram;

namespace WzComparerR2Server.Controllers;

public class HomeController : Controller
{

    AvatarCanvas avatar;
    string query_result;

    [Route("")]
    public string Index() // TODO : ActionResult
    {
        var dir = Directory.GetCurrentDirectory();
        var path = Path.Combine(dir, "a.png");
        var imageFileStream = System.IO.File.OpenRead(path);
        return Program.wz.WzNode.nodes[0].text;
        // return base.File(imageFileStream,"image/png");
    }

    private String dfs(Wz_Node current_node)
    {
        String ret = "{";
        bool First = true;
        
        foreach(Wz_Node child_node in current_node.nodes)
        {
            if (First) First = false;
            else ret += ", ";
            ret += "\"" + child_node.text + "\": " + dfs(child_node);
        }
        return ret + "}";
    }

    private string get_code(Wz_Node root)
    {
        return "{\"" + root.text + "\": " + dfs(root) + "}";
    }

    [Route("code")]
    public string Code()
    {
        if(query_result == null) query_result = get_code(Program.wz.WzNode);
        return query_result;
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
