using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Primitives;
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
	public ActionResult Index() // TODO : ActionResult
	{
		return Ok("main");
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
	public ActionResult Avatar_Raw(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return GetAvatar(code, actionName, bs);
	}

	[Route("avatar")]
	public ActionResult Avatar(
		string? head,
		string? face,
		string? hair,
		string? cap,
		string? coat,
		string? longcoat,
		string? pants,
		string? shoes,
		string? glove,
		string? shield,
		string? cape,
		string? weapon,
		string? earrings,
		string? faceAccessory,
		string? eyeAccessory,
		string? actionName,
		bool? bs
	)
	{
		string code="2000";
		GearType? gearType = null;
		Add_X_request_ID();
		if (head != null)
		{
			gearType = get_geartype(head);
			if (gearType == null || gearType != GearType.head)
			{
				return BadRequest("Fail to load item(head)");
			}
			code += ","; code += head;
		}
		if (face != null)
		{
			gearType = get_geartype(face); 
			if (gearType == null || !Gear.IsFace((GearType)gearType))
			{
				return BadRequest("Fail to load item(face)");
			}
			code += ","; code += face;
		}
		if (hair != null)
		{
			gearType = get_geartype(hair); 
			if (gearType == null || !Gear.IsHair((GearType)gearType))
			{
				return BadRequest("Fail to load item(hair)");
			}
			code += ","; code += hair;
		}
		if (cap != null)
		{
			gearType = get_geartype(cap); 
			if (gearType == null || gearType != GearType.cap)
			{
				return BadRequest("Fail to load item(cap)");
			}
			code += ","; code += cap;
		}
		if (coat != null)
		{
			gearType = get_geartype(coat); 
			if (gearType == null || gearType != GearType.coat)
			{
				return BadRequest("Fail to load item(coat)");
			}
			code += ","; code += coat;
		}
		if (longcoat != null)
		{
			gearType = get_geartype(longcoat); 
			if (gearType == null || gearType != GearType.longcoat)
			{
				return BadRequest("Fail to load item(longcoat)");
			}
			code += ","; code += longcoat;
		}
		if (pants != null)
		{
			gearType = get_geartype(pants); 
			if (gearType == null || gearType != GearType.pants)
			{
				return BadRequest("Fail to load item(pants)");
			}
			code += ","; code += pants;
		}
		if (shoes != null)
		{
			gearType = get_geartype(shoes); 
			if (gearType == null || gearType != GearType.shoes)
			{
				return BadRequest("Fail to load item(shoes)");
			}
			code += ","; code += shoes;
		}
		if (glove != null)
		{
			gearType = get_geartype(glove); 
			if (gearType == null || gearType != GearType.glove)
			{
				return BadRequest("Fail to load item(glove)");
			}
			code += ","; code += glove;
		}
		if (shield != null)
		{
			gearType = get_geartype(shield);
			if (gearType == null || gearType != GearType.shield)
			{
				return BadRequest("Fail to load item(shield)");
			}
			code += ","; code += shield;
		}
		if (cape != null)
		{
			gearType = get_geartype(cape); 
			if (gearType == null || gearType != GearType.cape)
			{
				return BadRequest("Fail to load item(cape)");
			}
			code += ","; code += cape;
		}
		if (weapon != null)
		{
			gearType = get_geartype(weapon);
			if (gearType == null || !Gear.IsWeapon((GearType)gearType) && gearType!=GearType.cashWeapon)
			{
				return BadRequest("Fail to load item(weapon)");
			}
			code += ","; code += weapon;
		}
		if (earrings != null)
		{
			gearType = get_geartype(earrings); 
			if (gearType == null || gearType != GearType.earrings)
			{
				return BadRequest("Fail to load item(earrings)");
			}
			code += ","; code += earrings;
		}
		if (faceAccessory != null)
		{
			gearType = get_geartype(faceAccessory);
			if (gearType == null || gearType != GearType.faceAccessory)
			{
				return BadRequest("Fail to load item(faceAccessory)");
			}
			code += ","; code += faceAccessory;
		}
		if (eyeAccessory != null)
		{
			gearType = get_geartype(eyeAccessory); 
			if (gearType == null || gearType != GearType.eyeAccessory)
			{
				return BadRequest("Fail to load item(eyeAccessory)");
			}
			code += ","; code += eyeAccessory;
		}
		if (longcoat != null && (coat != null || pants != null))
		{
			return BadRequest("longcoat and coat + pants can't be load simultaneously");
		}
		if (actionName != "stand1" && actionName != "stand2")
		{
			actionName = "stand1";
		}
		return GetAvatar(code, actionName, bs);
	}

	[Route("head")]
	public ActionResult Head(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.head, "head", bs);
	}

	[Route("face")]
	public ActionResult Face(string code, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithEmotion(code, GearType.face, "face", bs);
	}

	[Route("hair")]
	public ActionResult Hair(string code, string actionName, bool? bs)
	{
		var m = GetFromCode(code); Add_X_request_ID();
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
			var byteArray = BitmapToByteArray(this.avatar.MixBitmaps(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap,BitmapOrigin.CreateFromNode(mix_node, PluginManager.FindWz).Bitmap,mixOpacity));
			if (bs == true) return Content(Convert.ToBase64String(byteArray));
			else return base.File(byteArray,"image/png");
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
			var byteArray = BitmapToByteArray(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap);
			if (bs == true) return Content(Convert.ToBase64String(byteArray));
			return base.File(byteArray,"image/png");
		}
	}

	[Route("hairoverhead")]
	public ActionResult HairOverHead(string code, string actionName, bool? bs)
	{
		var m = GetFromCode(code); Add_X_request_ID();
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
			var byteArray = BitmapToByteArray(this.avatar.MixBitmaps(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap,BitmapOrigin.CreateFromNode(mix_node, PluginManager.FindWz).Bitmap,mixOpacity));
			if (bs == true) return Content(Convert.ToBase64String(byteArray));
			else return base.File(byteArray,"image/png");
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

			var byteArray = BitmapToByteArray(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap);
			if (bs == true) return Content(Convert.ToBase64String(byteArray));
			return base.File(byteArray,"image/png");
		}
	}

	[Route("cap")]
	public ActionResult Cap(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.cap, "default", bs);
	}

	[Route("coat")]
	public ActionResult Coat(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.coat, "mail", bs);
	}

	[Route("longcoat")]
	public ActionResult Longcoat(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.longcoat, "mail", bs);
	}

	[Route("pants")]
	public ActionResult Pants(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.pants, "pants", bs);
	}

	[Route("shoes")]
	public ActionResult Shoes(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.shoes, "shoes", bs);
	}

	[Route("lglove")]
	public ActionResult lGlove(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.glove, "lGlove", bs);
	}

	[Route("rglove")]
	public ActionResult rGlove(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.glove, "rGlove", bs);
	}

	[Route("shield")]
	public ActionResult Shield(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.shield, "shield", bs);
	}

	[Route("cape")]
	public ActionResult Cape(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.cape, "default", bs);
	}

	[Route("weapon")]
	public ActionResult Weapon(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.weapon, "weapon", bs);
	}

	[Route("earrings")]
	public ActionResult Earrings(string code, string actionName, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithAction(code, actionName, GearType.earrings, "default", bs);
	}

	[Route("faceAccessory")]
	public ActionResult FaceAccessory(string code, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithEmotion(code, GearType.faceAccessory, "default", bs);
	}

	[Route("eyeAccessory")]
	public ActionResult EyeAccessory(string code, bool? bs)
	{
		Add_X_request_ID();
		return ItemWithEmotion(code, GearType.eyeAccessory, "default", bs);
	}

	void Add_X_request_ID()
	{
		foreach (var header in Request.Headers)
		{
			if (header.Key == "X-Request-ID")
			{
				Response.Headers.Add(header.Key, header.Value);
				return;
			}
		}
		Response.Headers.Add("X-Request-ID", System.Guid.NewGuid().ToString());
	}

	GearType? get_geartype(string code)
	{
		var m = GetFromCode(code);
		if (m == null)
		{
			return null;
		}
		Wz_Node imgNode = GetWzNode(m);
		if (imgNode == null)
		{
			return null;
		}
		AvatarPart part = new AvatarPart(imgNode);
		return Gear.GetGearType(part.ID.Value);
	}

	private ActionResult ItemWithAction(string code, string actionName, GearType type, string typename, bool? bs)
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
		if(gearType != type && (type != GearType.weapon || !Gear.IsWeapon(gearType) && gearType != GearType.cashWeapon))
		{
			Console.WriteLine("Type mismatch : " + gearType.ToString());
			return BadRequest("item type mismatch");
		}
		var part_node = part.Node;
		if (gearType == GearType.cashWeapon)
		{
			bool finished = false;
			foreach (var node in part.Node.Nodes)
			{
				int typeID;
				if (Int32.TryParse(node.Text, out typeID))
				{
					foreach (var cnode in node.Nodes)
					{
						if(cnode.Text == actionName)
						{
							finished = true;
							part_node = cnode;
						}
					}
					if(finished)
					{
						break;
					}
				}
			}
			if (!finished)
			{
				Console.WriteLine("Action Not Found");
				return BadRequest("Action Not Found");
			}
			while(part_node.Value is Wz_Uol)
			{
				part_node = part_node.GetValue<Wz_Uol>().HandleUol(part_node);
			}
			var effect_node = part_node.FindNodeByPath("0").FindNodeByPath("effect");
			part_node = part_node.FindNodeByPath("0").FindNodeByPath(typename);
			if (effect_node != null)
			{
				var part_bitmap = BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz);
				var effect_bitmap = BitmapOrigin.CreateFromNode(effect_node, PluginManager.FindWz);
				var rect = new Rectangle(part_bitmap.OpOrigin, part_bitmap.Bitmap.Size);
				var newRect = new Rectangle(effect_bitmap.OpOrigin, effect_bitmap.Bitmap.Size);
                rect = Rectangle.Union(rect, newRect);
				
				Bitmap bmp = new Bitmap(rect.Width, rect.Height, System.Drawing.Imaging.PixelFormat.Format32bppArgb);
				Graphics g = Graphics.FromImage(bmp);
				g.DrawImage(effect_bitmap.Bitmap, effect_bitmap.OpOrigin.X - rect.X, effect_bitmap.OpOrigin.Y - rect.Y);
				g.DrawImage(part_bitmap.Bitmap, part_bitmap.OpOrigin.X - rect.X, part_bitmap.OpOrigin.Y - rect.Y);
				g.Dispose();
				if (bs == true) return Content(Convert.ToBase64String(BitmapToByteArray(bmp)));
				return base.File(BitmapToByteArray(bmp),"image/png");
			}
		}
		else 
		{
			part_node = part.Node.FindNodeByPath(actionName);
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
		}
		var byteArray = BitmapToByteArray(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap);
		if (bs == true) return Content(Convert.ToBase64String(byteArray));
		return base.File(byteArray,"image/png");
	}

	private ActionResult ItemWithEmotion(string code, GearType type, string typename, bool? bs)
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

		var byteArray = BitmapToByteArray(BitmapOrigin.CreateFromNode(part_node, PluginManager.FindWz).Bitmap);
		if (bs == true) return Content(Convert.ToBase64String(byteArray));
		return base.File(byteArray,"image/png");
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

	private ActionResult GetAvatar(string code, string actionName, bool? bs)
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
			var byteArray = BitmapToByteArray(frame.Bitmap);
			if (bs == true) return Content(Convert.ToBase64String(byteArray));
			return base.File(byteArray,"image/png");
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
