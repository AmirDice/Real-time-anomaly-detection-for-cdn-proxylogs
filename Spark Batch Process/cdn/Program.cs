using Microsoft.Spark.Sql;
using System;
using static Microsoft.Spark.Sql.Functions;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

namespace cdn
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var sparkSession = SparkSession.Builder().GetOrCreate();

            var options = new Dictionary<string, string>
            {
                {"delimiter","," }
            };
            var schemaString = "timestamp STRING, Status_code INT," +
                " contenttype STRING, protocol STRING, " +
                "contentlength DOUBLE, timefirstbyte FLOAT," +
                " timetoserv FLOAT, maxage INT, osfamily INT," +
                " sid INT, cachecontrol STRING, uamajor INT, uafamily" +
                " INT, devicefamily INT, fragment STRING, path INT," +
                " Content_Package INT, geo_location INT, Live_channel" +
                " INT, devicemodel INT, devicebrand INT, Host INT," +
                " method STRING, assetnumber INT, hit STRING," +
                " cachename INT, uid INT";
            var csvFile = sparkSession.Read()
                .Format("csv")
                .Options(options)
                .Schema(schemaString)
                .Load(@"C:\Users\aizaz\source\repos\cdn\cdn\dataset.csv");


            csvFile.PrintSchema();
            csvFile.Show(20);

            // Drop any row with N/A value if colum is N/A
            DataFrameNaFunctions dropEmptyProject = csvFile.Na();
            DataFrame cleanedProjects = dropEmptyProject.Drop("all");

            //Remove unncessary colums
            cleanedProjects = cleanedProjects.Drop("osfamily", "sid", "cachecontrol",
                "uamajor", "uafamily", "devicefamily", "fragment", "Content_Package",
                "devicemodel", "devicebrand", "method", "assetnumber", "cachename", "uid");
            cleanedProjects.Show(20);

            // Drop any row with N/A
            DataFrameNaFunctions dropEmptyProjectList = cleanedProjects.Na();
            DataFrame cleandProject1 = dropEmptyProjectList.Drop("any");
            cleandProject1.Show(20);

            // Rewrite it different do not use same location other-wise it delete working directory

            cleandProject1.Write()
                .Mode(SaveMode.Overwrite)
                .Option("header", true)
                .Option("NullValue","Null")
                .Csv(@"G:\Users\aizaz\source\repos\cdn\cdn");




            sparkSession.Stop();




        }
    }
}
