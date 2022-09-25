using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using WzComparerR2Server.Models;
using WzComparerR2;
using WzComparerR2.Common;
using WzComparerR2.Avatar;
using WzComparerR2.WzLib;
using WzComparerR2.PluginBase;
using MainProgram;
using System;
using System.Text;
using System.Text.RegularExpressions;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace WzComparerR2Server.Controllers;

public class HomeController : Controller
{

	AvatarCanvas avatar;
	string query_result;
	bool inited;
	public StringLinker DefaultStringLinker;

	public HomeController()
	{
		this.avatar = new AvatarCanvas();
		this.DefaultStringLinker = new StringLinker();
	}

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

	[Route("avatar")]
	public ActionResult Avatar(string code)
	{
		Console.WriteLine("Avatar 진입");
		if(LoadCode(code, 0)) {
			Console.WriteLine("성공");
			var bone = this.avatar.CreateFrame(0, 0, 0);
			var frame = this.avatar.DrawFrame(bone);
			frame.Bitmap.Save(Path.Combine(Directory.GetCurrentDirectory(), "b.png"), System.Drawing.Imaging.ImageFormat.Png);
			return base.File(BitmapToByteArray(frame.Bitmap),"image/png");
		}
		Console.WriteLine("실패");
		var dir = Directory.GetCurrentDirectory();
		var path = Path.Combine(dir, "a.png");
		var imageFileStream = System.IO.File.OpenRead(path);
		return base.File(imageFileStream,"image/png");
	}

	public static byte[] BitmapToByteArray(Bitmap bitmap)
	{
		byte[] result = null;
		if(bitmap != null)
		{
			MemoryStream stream = new MemoryStream();
			bitmap.Save(stream, bitmap.RawFormat);
			result = stream.ToArray();
		}
		else
		{
			Console.WriteLine("Bitmap is null.");
		}
		return result;

	}

	private bool AvatarInit()
	{
		Console.WriteLine("AvatarInit 실행");
		this.inited = this.avatar.LoadZ()
			&& this.avatar.LoadActions()
			&& this.avatar.LoadEmotions();
		avatar.ActionName = "stand1";
		avatar.EmotionName = "default";
		avatar.HairCover = true;
		return this.inited;
	}

	private bool LoadCode(string code, int loadType)
	{
		//解析
		var matches = Regex.Matches(code, @"s?(\d+)(\+([0-7])\*(\d{1,2}))?([,\s]|$)");
		if (matches.Count <= 0)
		{
			Console.WriteLine("아이템 코드에 해당되는 아이템이 없습니다.");
			return false;
		}

		if (PluginManager.FindWz(Wz_Type.Base) == null)
		{
			Console.WriteLine("Base.wz 파일을 열 수 없습니다.");
			return false;
		}

		var characWz = PluginManager.FindWz(Wz_Type.Character);
		var skillWz = PluginManager.FindWz(Wz_Type.Skill);
		var itemWz = PluginManager.FindWz(Wz_Type.Item);

		//试图初始化
		if (!this.inited && !this.AvatarInit())
		{
			Console.WriteLine("아바타 플러그인을 초기화할 수 없습니다.");
			return false;
		}
		var sl = this.DefaultStringLinker;
		if (!sl.HasValues) //生成默认stringLinker
		{
			sl.Load(PluginManager.FindWz(Wz_Type.String).GetValueEx<Wz_File>(null), PluginManager.FindWz(Wz_Type.Item).GetValueEx<Wz_File>(null), PluginManager.FindWz(Wz_Type.Etc).GetValueEx<Wz_File>(null));
		}

		if (loadType == 0) //先清空。。
		{
			Array.Clear(this.avatar.Parts, 0, this.avatar.Parts.Length);
		}

		List<int> failList = new List<int>();

		foreach (Match m in matches)
		{
			int gearID;
			if (Int32.TryParse(m.Result("$1"), out gearID))
			{
				Wz_Node imgNode = FindNodeByGearID(characWz, gearID);
				if (imgNode != null)
				{
					var part = this.avatar.AddPart(imgNode);
					if (m.Groups.Count >= 4 && Int32.TryParse(m.Result("$3"), out int mixColor) && Int32.TryParse(m.Result("$4"), out int mixOpacity))
					{
						part.MixColor = mixColor;
						part.MixOpacity = mixOpacity;
					}
					OnNewPartAdded(part);
					continue;
				}
				if (m.ToString().StartsWith("s"))
				{
					imgNode = FindNodeBySkillID(skillWz, gearID);
					if (imgNode != null)
					{
						int tamingMobID = imgNode.Nodes["vehicleID"].GetValueEx<int>(0);
						if (tamingMobID == 0)
						{
							tamingMobID = PluginManager.FindWz(string.Format(@"Skill\RidingSkillInfo.img\{0:D7}\vehicleID", gearID)).GetValueEx<int>(0);
						}
						if (tamingMobID != 0)
						{
							var tamingMobNode = PluginManager.FindWz(string.Format(@"Character\TamingMob\{0:D8}.img", tamingMobID));
							if (tamingMobNode != null)
							{
								var part = this.avatar.AddTamingPart(tamingMobNode, BitmapOrigin.CreateFromNode(imgNode.Nodes["icon"], PluginManager.FindWz), gearID, true);
								OnNewPartAdded(part);
							}
						}
						continue;
					}
				}
				imgNode = FindNodeByItemID(itemWz, gearID);
				if (imgNode != null)
				{
					int tamingMobID = imgNode.FindNodeByPath("info\\tamingMob").GetValueEx<int>(0);
					if (tamingMobID != 0)
					{
						var tamingMobNode = PluginManager.FindWz(string.Format(@"Character\TamingMob\{0:D8}.img", tamingMobID));
						if (tamingMobNode != null)
						{
							var part = this.avatar.AddTamingPart(tamingMobNode, BitmapOrigin.CreateFromNode(imgNode.FindNodeByPath("info\\icon"), PluginManager.FindWz), gearID, false);
							OnNewPartAdded(part);
						}
					}
					continue;
				}
				// else
				{
					failList.Add(gearID);
				}
			}
		}

		//刷新

		//其他提示
		if (failList.Count > 0)
		{
			StringBuilder sb = new StringBuilder();
			sb.AppendLine("해당 아이템 코드를 찾을 수 없습니다 : ");
			foreach (var gearID in failList)
			{
				sb.Append("  ").AppendLine(gearID.ToString("D8"));
			}
			Console.WriteLine(sb.ToString());
		}
		return true;
	}
	private Wz_Node FindNodeByGearID(Wz_Node characWz, int id)
	{
		string imgName = id.ToString("D8") + ".img";
		Wz_Node imgNode = null;

		foreach (var node1 in characWz.Nodes)
		{
			if (node1.Text == imgName)
			{
				imgNode = node1;
				break;
			}
			else if (node1.Nodes.Count > 0)
			{
				foreach (var node2 in node1.Nodes)
				{
					if (node2.Text == imgName)
					{
						imgNode = node2;
						break;
					}
				}
				if (imgNode != null)
				{
					break;
				}
			}
		}

		if (imgNode != null)
		{
			Wz_Image img = imgNode.GetValue<Wz_Image>();
			if (img != null && img.TryExtract())
			{
				return img.Node;
			}
		}

		return null;
	}

	private Wz_Node FindNodeBySkillID(Wz_Node skillWz, int id)
	{
		string idName = id.ToString();

		foreach (var node1 in skillWz.Nodes)
		{
			if (idName.StartsWith(node1.Text.Replace(".img", "")))
			{
				Wz_Image img = node1.GetValue<Wz_Image>();
				if (img != null && img.TryExtract())
				{
					if (img.Node.Nodes["skill"].Nodes.Count > 0)
					{
						foreach (var skillNode in img.Node.Nodes["skill"].Nodes)
						{
							if (skillNode.Text == idName)
							{
								return skillNode;
							}
						}
					}
				}
			}
		}

		return null;
	}


	private Wz_Node FindNodeByItemID(Wz_Node itemWz, int id)
	{
		string idName = id.ToString("D8");
		Wz_Node imgNode = null;

		foreach (var node1 in itemWz.Nodes)
		{
			if (node1.Nodes.Count > 0)
			{
				foreach (var node2 in node1.Nodes)
				{
					if (idName.StartsWith(node2.Text.Replace(".img", "")))
					{
						imgNode = node2;
						break;
					}
				}
				if (imgNode != null)
				{
					break;
				}
			}
		}

		if (imgNode != null)
		{
			Wz_Image img = imgNode.GetValue<Wz_Image>();
			if (img != null && img.TryExtract())
			{
				if (img.Node.Nodes.Count > 0)
				{
					foreach (var itemNode in img.Node.Nodes)
					{
						if (itemNode.Text == idName)
						{
							return itemNode;
						}
					}
				}
			}
		}

		return null;
	}

	private void OnNewPartAdded(AvatarPart part)
	{
		if (part == null)
		{
			return;
		}

		if (part == avatar.Body) //同步head
		{
			int headID = 10000 + part.ID.Value % 10000;
			if (avatar.Head == null || avatar.Head.ID != headID)
			{
				var headImgNode = PluginManager.FindWz(string.Format("Character\\{0:D8}.img", headID));
				if (headImgNode != null)
				{
					this.avatar.AddPart(headImgNode);
				}
			}
		}
		else if (part == avatar.Head) //同步body
		{
			int bodyID = part.ID.Value % 10000;
			if (avatar.Body == null || avatar.Body.ID != bodyID)
			{
				var bodyImgNode = PluginManager.FindWz(string.Format("Character\\{0:D8}.img", bodyID));
				if (bodyImgNode != null)
				{
					this.avatar.AddPart(bodyImgNode);
				}
			}
		}
		else if (part == avatar.Face) //同步表情
		{
			this.avatar.LoadEmotions();
		}
		else if (part == avatar.Taming) //同步座驾动作
		{
			this.avatar.LoadTamingActions();
		}
		else if (part == avatar.Pants || part == avatar.Coat) //隐藏套装
		{
			if (avatar.Longcoat != null)
			{
				avatar.Longcoat.Visible = false;
			}
		}
		else if (part == avatar.Longcoat) //还是。。隐藏套装
		{
			if (avatar.Pants != null && avatar.Pants.Visible
				|| avatar.Coat != null && avatar.Coat.Visible)
			{
				avatar.Longcoat.Visible = false;
			}
		}
	}
}
