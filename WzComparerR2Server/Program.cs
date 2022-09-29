using WzComparerR2;
using WzComparerR2.WzLib;
using WzComparerR2.PluginBase;


namespace MainProgram
{
public class Program
{

	public static Wz_Structure wz;
	public static List<Wz_Structure> openedWz;
	static void Main(string[] args)
	{
		System.AppContext.SetSwitch("System.Drawing.EnableUnixSupport", true);

		PluginManager.WzFileFinding += new FindWzEventHandler(CharaSimLoader_WzFileFinding);

		var dir = Path.Combine(Path.Combine(Directory.GetCurrentDirectory(), "Data"), "Data");
		var wzFilePath = Path.Combine(Path.Combine(dir, "Base"), "Base.wz");

		wz = new Wz_Structure();
		openedWz = new List<Wz_Structure>();

		Console.WriteLine("Load Start");

		if (wz.IsKMST1125WzFormat(wzFilePath))
		{
			wz.LoadKMST1125DataWz(wzFilePath);
		}
		else
		{
			wz.Load(wzFilePath, true);
		}

		openedWz.Add(wz);

		Console.WriteLine("Load Complete");

		foreach (string arg in args)
		{
			Console.WriteLine(arg);
		}

		var builder = WebApplication.CreateBuilder(args);

		// Add services to the container.
		builder.Services.AddControllersWithViews();

		var app = builder.Build();

		// Configure the HTTP request pipeline.
		if (!app.Environment.IsDevelopment())
		{
			app.UseExceptionHandler("/Home/Error");
			// The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
			app.UseHsts();
		}

		app.UseHttpsRedirection();
		app.UseStaticFiles();

		app.UseRouting();

		app.UseAuthorization();

		app.MapControllerRoute(
			name: "default",
			pattern: "{controller=Home}/{action=Index}/{id?}");

		app.MapControllerRoute(
			name: "code",
			pattern: "{controller=Home}/{action=Code}");

		app.MapControllerRoute(
			name: "avatar",
			pattern: "{controller=Home}/{action=Avatar}");

		app.MapControllerRoute(
			name: "avatar_raw",
			pattern: "{controller=Home}/{action=Avatar_Raw}");

		app.MapControllerRoute(
			name: "head",
			pattern: "{controller=Home}/{action=Head}");

		app.MapControllerRoute(
			name: "face",
			pattern: "{controller=Home}/{action=Face}");

		app.MapControllerRoute(
			name: "hair",
			pattern: "{controller=Home}/{action=Hair}");

		app.MapControllerRoute(
			name: "hairoverhead",
			pattern: "{controller=Home}/{action=HairOverHead}");

		app.MapControllerRoute(
			name: "coat",
			pattern: "{controller=Home}/{action=Coat}");

		app.MapControllerRoute(
			name: "longcoat",
			pattern: "{controller=Home}/{action=Longcoat}");

		app.MapControllerRoute(
			name: "pants",
			pattern: "{controller=Home}/{action=Pants}");

		app.MapControllerRoute(
			name: "shoes",
			pattern: "{controller=Home}/{action=Shoes}");

		app.MapControllerRoute(
			name: "lglove",
			pattern: "{controller=Home}/{action=lGlove}");

		app.MapControllerRoute(
			name: "rglove",
			pattern: "{controller=Home}/{action=rGlove}");

		app.MapControllerRoute(
			name: "shield",
			pattern: "{controller=Home}/{action=Shield}");

		app.MapControllerRoute(
			name: "cape",
			pattern: "{controller=Home}/{action=Cape}");

		app.MapControllerRoute(
			name: "weapon",
			pattern: "{controller=Home}/{action=Weapon}");

		app.MapControllerRoute(
			name: "earrings",
			pattern: "{controller=Home}/{action=Earrings}");

		app.MapControllerRoute(
			name: "faceAccessory",
			pattern: "{controller=Home}/{action=FaceAccessory}");

		app.MapControllerRoute(
			name: "eyeAccessory",
			pattern: "{controller=Home}/{action=EyeAccessory}");

		app.Run();
	}

	static void CharaSimLoader_WzFileFinding(object sender, FindWzEventArgs e)
	{
		string[] fullPath = null;
		if (!string.IsNullOrEmpty(e.FullPath)) //用fullpath作为输入参数
		{
			fullPath = e.FullPath.Split('/', '\\');
			e.WzType = Enum.TryParse<Wz_Type>(fullPath[0], true, out var wzType) ? wzType : Wz_Type.Unknown;
		}

		List<Wz_Node> preSearch = new List<Wz_Node>();
		if (e.WzType != Wz_Type.Unknown) //用wztype作为输入参数
		{
			IEnumerable<Wz_Structure> preSearchWz = e.WzFile?.WzStructure != null ?
				Enumerable.Repeat(e.WzFile.WzStructure, 1) :
				openedWz;
			foreach (var wzs in preSearchWz)
			{
				Wz_File baseWz = null;
				bool find = false;
				foreach (Wz_File wz_f in wzs.wz_files)
				{
					if (wz_f.Type == e.WzType)
					{
						preSearch.Add(wz_f.Node);
						find = true;
						//e.WzFile = wz_f;
					}
					if (wz_f.Type == Wz_Type.Base)
					{
						baseWz = wz_f;
					}
				}

				// detect data.wz
				if (baseWz != null && !find)
				{
					string key = e.WzType.ToString();
					foreach (Wz_Node node in baseWz.Node.Nodes)
					{
						if (node.Text == key && node.Nodes.Count > 0)
						{
							preSearch.Add(node);
						}
					}
				}
			}
		}

		if (fullPath == null || fullPath.Length <= 1)
		{
			if (e.WzType != Wz_Type.Unknown && preSearch.Count > 0) //返回wzFile
			{
				e.WzNode = preSearch[0];
				e.WzFile = preSearch[0].Value as Wz_File;
			}
			return;
		}

		if (preSearch.Count <= 0)
		{
			return;
		}

		foreach (var wzFileNode in preSearch)
		{
			var searchNode = wzFileNode;
			for (int i = 1; i < fullPath.Length && searchNode != null; i++)
			{
				searchNode = searchNode.Nodes[fullPath[i]];
				var img = searchNode.GetValueEx<Wz_Image>(null);
				if (img != null)
				{
					searchNode = img.TryExtract() ? img.Node : null;
				}
			}

			if (searchNode != null)
			{
				e.WzNode = searchNode;
				e.WzFile = wzFileNode.Value as Wz_File;
				return;
			}
		}
		//寻找失败
		e.WzNode = null;
	}

}

}