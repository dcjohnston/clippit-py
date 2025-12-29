using Clippit;
using Clippit.Word;

if (args.Length < 4)
{
    Console.Error.WriteLine("Usage: clippit-compare <author> <original.docx> <modified.docx> <output.docx>");
    Console.Error.WriteLine("  author      - Author name for tracked changes");
    Console.Error.WriteLine("  original    - Path to original document");
    Console.Error.WriteLine("  modified    - Path to modified document");
    Console.Error.WriteLine("  output      - Path for output document with tracked changes");
    Environment.Exit(1);
}

var author = args[0];
var originalPath = args[1];
var modifiedPath = args[2];
var outputPath = args[3];

try
{
    if (!File.Exists(originalPath))
    {
        Console.Error.WriteLine($"Error: Original file not found: {originalPath}");
        Environment.Exit(2);
    }
    if (!File.Exists(modifiedPath))
    {
        Console.Error.WriteLine($"Error: Modified file not found: {modifiedPath}");
        Environment.Exit(2);
    }

    var source1 = new WmlDocument(originalPath);
    var source2 = new WmlDocument(modifiedPath);

    var settings = new WmlComparerSettings
    {
        AuthorForRevisions = author,
        DetailThreshold = 0
    };

    var result = WmlComparer.Compare(source1, source2, settings);
    result.SaveAs(outputPath);

    Console.WriteLine($"Comparison complete. Output written to: {outputPath}");
    Environment.Exit(0);
}
catch (Exception ex)
{
    Console.Error.WriteLine($"Error during comparison: {ex.Message}");
    Console.Error.WriteLine(ex.StackTrace);
    Environment.Exit(3);
}
