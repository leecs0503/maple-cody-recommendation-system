using WzComparerR2.WzLib;


namespace MainProgram
{
public class Program
{

    public static Wz_Structure wz;
    static void Main(string[] args)
    {
        var dir = Path.Combine(Directory.GetCurrentDirectory(), "Data");
        var wzFilePath = Path.Combine(Path.Combine(dir, "Base"), "Base.wz");

        wz = new Wz_Structure();
        if (wz.IsKMST1125WzFormat(wzFilePath))
        {
            wz.LoadKMST1125DataWz(wzFilePath);
        }
        else
        {
            wz.Load(wzFilePath, true);
        }

        Console.Write("Load Complete\n");

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
            pattern: "{controller=Home}/{action=Code}/{id?}");

        app.Run();
    }
}

}