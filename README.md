URLscrapper Maltego Transforms

The URLscrapper Maltego transforms are a set of two transforms, namely 'fromURL' and 'fromWebsite,' created by HawkeEyes. These transforms expand on the functionality of the Uscrapper tool developed by z0m31en (available at https://github.com/z0m31en). They enable the extraction of valuable information from URLs and websites within the Maltego environment.

The 'fromURL' transform can be applied to a maltego.URL entity, while the 'fromWebsite' transform is designed for maltego.Website entities. When executed, both transforms generate outputs in the form of "maltego.Person," "maltego.Email," "maltego.PhoneNumber," "maltego.Location," and "maltego.URL" entities.

To install these transforms in your Maltego client, follow these steps:

Open a terminal and navigate to the directory where you wish to store the transform files.
Run the following commands:

    git clone https://github.com/HawkEyes-OSINT/URLscrapperTransform.git
    cd URLscrapperTransform
    pip install -r requirements.txt
    python project.py run

After executing these commands, a file named URLscrapper.mtz will be available in your directory.

To import the transforms into your Maltego client, proceed as follows:

Open your Maltego client and navigate to the 'Import/Export' tab.
Click on 'Import Config.'
Select the file 'URLscrapper.mtz.'

By following these steps, you will successfully install the URLscrapper transforms on your Maltego client.

For more information or support, please visit HawkeEyes at https://hawk-eyes.io.
