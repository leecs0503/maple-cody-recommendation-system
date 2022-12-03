namespace WzComparerR2Server.Models;

public class ItemListModel
{
    public string? RequestId { get; set; }

    public bool ShowRequestId => !string.IsNullOrEmpty(RequestId);
}
