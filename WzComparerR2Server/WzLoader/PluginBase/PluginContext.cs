using System;
using System.Collections.Generic;
using System.Text;
using WzComparerR2.WzLib;
using WzComparerR2.Common;
using DevComponents.DotNetBar;
using WzComparerR2.Controls;

namespace WzComparerR2.PluginBase
{
    public class PluginContext
    {
        internal PluginContext()
        {
            DefaultStringLinker = new StringLinker();
        }

        public StringLinker DefaultStringLinker;
    }
}
