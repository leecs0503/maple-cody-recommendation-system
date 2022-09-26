using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using WzComparerR2Server.Models;
using WzComparerR2;
using WzComparerR2.Common;
using WzComparerR2.Avatar;
using WzComparerR2.WzLib;
using WzComparerR2.PluginBase;
using WzComparerR2.CharaSim;
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
		return Program.wz.WzNode.Nodes[0].Text;
		// return base.File(imageFileStream,"image/png");
	}

	private String dfs(Wz_Node current_node)
	{
		String ret = "{";
		bool First = true;
		
		foreach(Wz_Node child_node in current_node.Nodes)
		{
			if (First) First = false;
			else ret += ", ";
			ret += "\"" + child_node.Text + "\": " + dfs(child_node);
		}
		return ret + "}";
	}

	private string get_code(Wz_Node root)
	{
		return "{\"" + root.Text + "\": " + dfs(root) + "}";
	}

	[Route("code")]
	public string Code()
	{
		if(query_result == null) query_result = get_code(Program.wz.WzNode);
		return query_result;
	}

	[Route("avatar_raw")]
	public ActionResult Avatar_Raw(string code, string actionName)
	{
		return GetAvatar(code, actionName);
	}

	[Route("avatar")]
	public ActionResult Avatar(string code, string actionName)
	{
		return GetAvatar(code, actionName);
	}

	[Route("head")]
	public ActionResult Head(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.head, "head");
	}

	[Route("face")]
	public ActionResult Face(string code)
	{
		return ItemWithEmotion(code, GearType.face, "face");
	}

	[Route("hair")]
	public ActionResult Hair(string code, string actionName)
	{
		var m = GetFromCode(code);
		if (m == null)
		{
			return BadRequest("Wrong Code");
		}
		if(actionName != "stand1" && actionName != "stand2")
		{
			actionName = "stand1";
		}
		Wz_Node imgNode = GetWzNode(m);
		if (imgNode == null)
		{
			Console.WriteLine("Image Node not found");
			return BadRequest("wz file not found");
		}
		AvatarPart part = new AvatarPart(imgNode);
		var gearType = Gear.GetGearType(part.ID.Value);
		if(gearType != GearType.hair && gearType != GearType.hair2 && gearType != GearType.hair3)
		{
			Console.WriteLine("Type mismatch : " + gearType.ToString());
			return BadRequest("item type mismatch");
		}
		if (m.Groups.Count >= 4 && Int32.TryParse(m.Result("$3"), out int mixColor) && Int32.TryParse(m.Result("$4"), out int mixOpacity))
		{
			part.MixColor = mixColor;
			part.MixOpacity = mixOpacity;
			var part_node = part.Node.FindNodeByPath(actionName);
			if (part_node == null)
			{
				Console.WriteLine("Action Not Found");
				return BadRequest("Action Not Found");
			}
			part_node = part_node.FindNodeByPath("0").FindNodeByPath("hair");
			var mix_node = part.MixNodes[mixColor].FindNodeByPath(actionName).FindNodeByPath("0").FindNodeByPath("hair");
			while(part_node.Value is Wz_Uol)
			{
				part_node = part_node.GetValue<Wz_Uol>().HandleUol(part_node);
			}
			return base.File(BitmapToByteArray(this.avatar.MixBitmaps(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap,BitmapOrigin.CreateFromNode(mix_node, PluginManager.FindWz).Bitmap,mixOpacity)),"image/png");
		}
		else
		{
			var part_node = part.Node.FindNodeByPath(actionName);
			if (part_node == null)
			{
				Console.WriteLine("Action Not Found");
				return BadRequest("Action Not Found");
			}
			part_node = part_node.FindNodeByPath("0").FindNodeByPath("hair");
			while(part_node.Value is Wz_Uol)
			{
				part_node = part_node.GetValue<Wz_Uol>().HandleUol(part_node);
			}

			return base.File(BitmapToByteArray(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap),"image/png");
		}
	}

	[Route("hairoverhead")]
	public ActionResult HairOverHead(string code, string actionName)
	{
		var m = GetFromCode(code);
		if (m == null)
		{
			return BadRequest("Wrong Code");
		}
		if(actionName != "stand1" && actionName != "stand2")
		{
			actionName = "stand1";
		}
		Wz_Node imgNode = GetWzNode(m);
		if (imgNode == null)
		{
			Console.WriteLine("Image Node not found");
			return BadRequest("wz file not found");
		}
		AvatarPart part = new AvatarPart(imgNode);
		var gearType = Gear.GetGearType(part.ID.Value);
		if(gearType != GearType.hair && gearType != GearType.hair2 && gearType != GearType.hair3)
		{
			Console.WriteLine("Type mismatch : " + gearType.ToString());
			return BadRequest("item type mismatch");
		}
		if (m.Groups.Count >= 4 && Int32.TryParse(m.Result("$3"), out int mixColor) && Int32.TryParse(m.Result("$4"), out int mixOpacity))
		{
			part.MixColor = mixColor;
			part.MixOpacity = mixOpacity;
			var part_node = part.Node.FindNodeByPath(actionName);
			if (part_node == null)
			{
				Console.WriteLine("Action Not Found");
				return BadRequest("Action Not Found");
			}
			part_node = part_node.FindNodeByPath("0").FindNodeByPath("hairOverHead");
			var mix_node = part.MixNodes[mixColor].FindNodeByPath(actionName).FindNodeByPath("0").FindNodeByPath("hairOverHead");
			while(part_node.Value is Wz_Uol)
			{
				part_node = part_node.GetValue<Wz_Uol>().HandleUol(part_node);
			}
			return base.File(BitmapToByteArray(this.avatar.MixBitmaps(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap,BitmapOrigin.CreateFromNode(mix_node, PluginManager.FindWz).Bitmap,mixOpacity)),"image/png");
		}
		else
		{
			var part_node = part.Node.FindNodeByPath(actionName);
			if (part_node == null)
			{
				Console.WriteLine("Action Not Found");
				return BadRequest("Action Not Found");
			}
			part_node = part_node.FindNodeByPath("0").FindNodeByPath("hairOverHead");
			while(part_node.Value is Wz_Uol)
			{
				part_node = part_node.GetValue<Wz_Uol>().HandleUol(part_node);
			}

			return base.File(BitmapToByteArray(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap),"image/png");
		}
	}

	[Route("cap")]
	public ActionResult Cap(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.cap, "default");
	}

	[Route("coat")]
	public ActionResult Coat(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.coat, "mail");
	}

	[Route("longcoat")]
	public ActionResult Longcoat(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.longcoat, "mail");
	}

	[Route("pants")]
	public ActionResult Pants(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.pants, "pants");
	}

	[Route("shoes")]
	public ActionResult Shoes(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.shoes, "shoes");
	}

	[Route("lglove")]
	public ActionResult lGlove(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.glove, "lGlove");
	}

	[Route("rglove")]
	public ActionResult rGlove(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.glove, "rGlove");
	}

	[Route("shield")]
	public ActionResult Shield(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.shield, "shield");
	}

	[Route("cape")]
	public ActionResult Cape(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.cape, "default");
	}

	[Route("weapon")]
	public ActionResult Weapon(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.weapon, "weapon");
	}

	[Route("earrings")]
	public ActionResult Earrings(string code, string actionName)
	{
		return ItemWithAction(code, actionName, GearType.earrings, "default");
	}

	[Route("faceAccessory")]
	public ActionResult FaceAccessory(string code)
	{
		return ItemWithEmotion(code, GearType.faceAccessory, "default");
	}

	[Route("eyeAccessory")]
	public ActionResult EyeAccessory(string code)
	{
		return ItemWithEmotion(code, GearType.eyeAccessory, "default");
	}

	private ActionResult ItemWithAction(string code, string actionName, GearType type, string typename)
	{
		var m = GetFromCode(code);
		if (m == null)
		{
			return BadRequest("Wrong Code");
		}
		if(actionName != "stand1" && actionName != "stand2")
		{
			actionName = "stand1";
		}
		Wz_Node imgNode = GetWzNode(m);
		if (imgNode == null)
		{
			Console.WriteLine("Image Node not found");
			return BadRequest("wz file not found");
		}
		AvatarPart part = new AvatarPart(imgNode);
		var gearType = Gear.GetGearType(part.ID.Value);
		if(gearType != type && (type != GearType.weapon || !Gear.IsWeapon(gearType)))
		{
			Console.WriteLine("Type mismatch : " + gearType.ToString());
			return BadRequest("item type mismatch");
		}
		var part_node = part.Node.FindNodeByPath(actionName);
		if (part_node == null)
		{
			Console.WriteLine("Action Not Found");
			return BadRequest("Action Not Found");
		}
		part_node = part_node.FindNodeByPath("0").FindNodeByPath(typename);
		while(part_node.Value is Wz_Uol)
		{
			part_node = part_node.GetValue<Wz_Uol>().HandleUol(part_node);
		}

		return base.File(BitmapToByteArray(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap),"image/png");
	}

	private ActionResult ItemWithEmotion(string code, GearType type, string typename)
	{
		var m = GetFromCode(code);
		if (m == null)
		{
			return BadRequest("Wrong Code");
		}
		Wz_Node imgNode = GetWzNode(m);
		if (imgNode == null)
		{
			Console.WriteLine("Image Node not found");
			return BadRequest("wz file not found");
		}
		AvatarPart part = new AvatarPart(imgNode);
		var gearType = Gear.GetGearType(part.ID.Value);
		if(gearType != type)
		{
			Console.WriteLine("Type mismatch : " + gearType.ToString());
			return BadRequest("item type mismatch");
		}
		var part_node = part.Node.FindNodeByPath("default").FindNodeByPath(typename);

		while(part_node.Value is Wz_Uol)
		{
			part_node = part_node.GetValue<Wz_Uol>().HandleUol(part_node);
		}

		return base.File(BitmapToByteArray(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap),"image/png");
	}

	Wz_Node? GetWzNode(Match m)
	{
		if (PluginManager.FindWz(Wz_Type.Base) == null)
		{
			Console.WriteLine("Base.wz 파일을 열 수 없습니다.");
			return null;
		}

		var characWz = PluginManager.FindWz(Wz_Type.Character);

		if (!this.inited && !this.AvatarInit())
		{
			Console.WriteLine("아바타 플러그인을 초기화할 수 없습니다.");
			return null;
		}
		int gearID;
		if (Int32.TryParse(m.Result("$1"), out gearID))
		{
			return FindNodeByGearID(characWz, gearID);
		}
		return null;
	}

	Match? GetFromCode(string code)
	{
		var matches = Regex.Matches(code, @"s?(\d+)(\+([0-7])\*(\d{1,2}))?([,\s]|$)");
		if (matches.Count <= 0)
		{
			Console.WriteLine("아이템 코드에 해당되는 아이템이 없습니다.");
			return null;
		}
		if (matches.Count != 1)
		{
			Console.WriteLine("잘못된 포맷입니다.");
			return null;
		}
		return matches[0];
	}

	private ActionResult GetAvatar(string code, string actionName)
	{
		Console.WriteLine("Avatar 진입 : " + code);
		if(actionName == "stand1" || actionName == "stand2")
		{
			avatar.ActionName = actionName;
		}
		else
		{
			avatar.ActionName = "stand1";
		}
		if(code != null && LoadCode(code, 0)) {
			Console.WriteLine("성공");
			var bone = this.avatar.CreateFrame(0, 0, 0);
			var frame = this.avatar.DrawFrame(bone);
			frame.Bitmap.Save(Path.Combine(Directory.GetCurrentDirectory(), "b.png"), System.Drawing.Imaging.ImageFormat.Png);
			return base.File(BitmapToByteArray(frame.Bitmap),"image/png");
		}
		Console.WriteLine("실패");
		return NotFound();
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
		this.inited = this.avatar.LoadZ()
			&& this.avatar.LoadActions()
			&& this.avatar.LoadEmotions();
		avatar.EmotionName = "default";
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
		bool HairCover = false;

		foreach (Match m in matches)
		{
			int gearID;
			if (Int32.TryParse(m.Result("$1"), out gearID))
			{
				Wz_Node imgNode = FindNodeByGearID(characWz, gearID);
				if (imgNode != null)
				{
					var part = this.avatar.AddPart(imgNode);
					AvatarPart avatar_part = new AvatarPart(imgNode);

					var gearType = Gear.GetGearType(avatar_part.ID.Value);

					if (gearType == GearType.cap && imgNode.Text != "01002186.img" && imgNode.Text != "01004109.img")
					{
						HairCover = true;
						
					}

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

		avatar.HairCover = HairCover;

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
		else if (part == avatar.Weapon) //同步武器类型
		{
			FillWeaponTypes();
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
	private void FillWeaponTypes()
    {
		if (this.avatar.Weapon != null && this.avatar.Weapon.ID != null && Gear.GetGearType(this.avatar.Weapon.ID.Value) == GearType.cashWeapon)
		{
			bool finished = false;
			foreach (var node in this.avatar.Weapon.Node.Nodes)
			{
				int typeID;
				if (Int32.TryParse(node.Text, out typeID))
				{
					foreach (var cnode in node.Nodes)
					{
						if(cnode.Text == avatar.ActionName)
						{
							finished = true;
							avatar.WeaponType = typeID;
						}
					}
					if(finished)
					{
						break;
					}
				}
			}
		}
    }
}
