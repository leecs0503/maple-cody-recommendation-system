using System;
using System.Collections.Generic;
using System.Text;
using DevComponents.DotNetBar;
using WzComparerR2.WzLib;
using WzComparerR2;
using WzComparerR2.Common;
using WzComparerR2.Controls;

namespace WzComparerR2.PluginBase
{
    internal interface PluginContextProvider
    {
        IList<Wz_Structure> LoadedWz { get; }
        StringLinker DefaultStringLinker { get; }
        event EventHandler<WzStructureEventArgs> WzOpened;
        event EventHandler<WzStructureEventArgs> WzClosing;
    }
}
