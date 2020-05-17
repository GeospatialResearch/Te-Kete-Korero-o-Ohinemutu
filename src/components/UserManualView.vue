<template>
  <div>
    <div id="CreateAUserAccount">
      <h5 class="mb-3">
        Create a user account
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          To create a new user account, click onto the Login button in the upper-right corner of the screen (marked with a red arrow in the image below), and then inside the popup click the link “Don’t have an account? Sign up”. To create an account you will be asked to provide a username, an email, a password and to confirm password.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/adduseraccount.png">
        </div>
        <div class="row mb-4 user-manual-p">
          After creating an account, you will receive an email with a link to verify that the email used exists and is valid. Clicking on the Verify Email link the account gets activated and you can now login as a General user.  This (Tātou access level) provides limited public access to the tool. This includes access to data and map layers which are in the public domain as well as cultural narratives provided by the Ōhinemutu community to the public.
        </div>
      </div>
    </div>
    <div id="IwiMembershipVerification">
      <h5 class="mb-3">
        Iwi membership verification
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          After creating a user account and verifying the email, you (as a Ngāti Whakaue member) can request membership verification. Membership verification provides registered Ngāti Whakaue members access to deeper levels of cultural narratives about Ōhinemutu, depending on their whakapapa and the Kōhanga nests to which they have right of access to. It also provides members the ability of to create and publish a range of narratives into a range of nests. To request the Ngāti Whakaue membership verification, you must be logged in and access your Profile page and press the button Request Iwi Membership verification. You will be then asked to complete a form with some private information about you such as Name, Ngāti Whakaue membership number, Date of Birth, Affiliations etc. and press the button ‘Send request’.
          <ul class="mt-2">
            <li>
              <b>Automatic verification:</b> Membership verification can be done automatically if the information provided by you matches the list of Iwi members provided by Ngāti Whakaue.
            </li>
            <li>
              <b>Manual verification:</b> If the information provided by you does not match a record in the list an email is sent to the administrator. The administrator will request further information and once satisfied, they will then set the appropriate levels of access for you manually.
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div id="MapNavigation">
      <h5 class="mb-3">
        Map navigation
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          The tools and shortcuts below can be used to navigate your way around the interactive map.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/mapnavigation.png">
        </div>
        <div class="row mb-4">
          <table class="align-center" style="width:100%;border-collapse: collapse;">
            <tr>
              <th colspan="2">
                Shotcuts
              </th>
            </tr>
            <tr>
              <td>Shift, right click, and drag</td>
              <td>Zoom to area of interest</td>
            </tr>
            <tr>
              <td>Right click and drag</td>
              <td>Pan</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
    <div id="Layers">
      <h5 class="mb-3">
        Layers
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          The Layers section allows users to load geographical information onto the map from several sources. There are three types of layers in the tool – My layers, External layers and Internal layers.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/layers.png">
        </div>
      </div>
    </div>
    <div id="MyLayers">
      <h5 class="mb-3">
        My layers
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          My layers refers to datasets that you, as an authenticated user, uploads into the tool. These datasets can be vector datasets (zipped shapefile or geoJSON file) or raster datasets (.tiff). Only the user who uploaded a dataset has access to this layers unless they share them with another user. In My layers section, the user can perform some actions to the uploaded layers including ‘Zoom to layer’, ‘Rename layer’, ‘Add copyright’, ‘Edit style’, ‘Share layer’ and ‘Delete layer’, clicking the vertical ellipsis button of the respective layer as shown in the picture below.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/mylayers.png">
        </div>
      </div>
    </div>
    <div id="ExternalLayers">
      <h5 class="mb-3">
        External layers
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          External layers refer to layers that the tool pulls from public dataset services provided by third-party organizations such as LINZ and MfE. These web services are managed by the providers and consequently the visibility of these data in the tool will be dependent of the availability of those services. These are ‘live’ updates, providing up-to-date information to the public as released by the provider. Every user of the tool has access to these layers.
        </div>
      </div>
    </div>
    <div id="InternalLayers">
      <h5 class="mb-3">
        Internal layers
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          Internal layers refer to datasets that the administrator uploads and makes available to every user of the tool. Like the External layers, the Internal layers usually come from third-party sources but in file format instead of web services, which means that these layers do not have ‘live’ updates, they are reliant on administration receiving and uploading updates as they become available (removing the layer and uploading a more updated version of the dataset). External and Internal layers are grouped according to Base layers, Political Boundaries, Topographic layers, Land use layers, and Māori relevant data.
        </div>
        <div class="row mb-4 user-manual-p">
          To activate and deactivate a layer, so the layer shows up on the map, check or uncheck the checkbox on the right side of the layer name.
        </div>
      </div>
    </div>
    <div id="Narratives">
      <h5 class="mb-3">
        Narratives
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          The Narratives section lists all the narratives that the user has access to, divided into two groups – My narratives and Other narratives.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/narratives.png">
        </div>
      </div>
    </div>
    <div id="MyNarratives">
      <h5 class="mb-3">
        My narratives
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          My narratives refer to narratives added or co-created by the authenticated user. Only authenticated users can add and co-create narratives.
        </div>
      </div>
    </div>
    <div id="OtherNarratives">
      <h5 class="mb-3">
        Other narratives
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          Other narratives refer to narratives, added by other users, that the authenticated user has right of access through whakapapa e.g. whanau, Koromātua, Ngāti Whakaue or because the narrative is published at the public Tātou level or it was shared with him/her.
          When unauthenticated, Other narratives becomes Public narratives since the unauthenticated user that accesses this list will only be able to read narratives published in the Tātou level (those narratives that the Ōhinemutu Development Working Group (ODWG) Incorporated Society wish to make available to the public).
        </div>
      </div>
    </div>
    <div id="AddNewNarrative">
      <h5 class="mb-3">
        Add new narrative
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          To add a new narrative click the ‘Add new narrative’ button on the left sidebar and a new narrative form opens up in a panel on the right side of the screen, as shown below.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/addnewnarrative.png">
        </div>
        <div class="row mb-4 user-manual-p">
          Below is a series of steps for you to create a new narrative. Click onto the links for more information.
          <ol class="mt-2">
            <li>Give your narrative a Title.</li>
            <li><a href="#" @click="scrollToUserManualSection('DateTheNarrative')">Date</a> your narrative. Options are precise date, precise year, year range or ancient.</li>
            <li>Connect your narrative to a <a href="#" @click="scrollToUserManualSection('NarrativeType')">Narrative type</a>. Options are Traditional narrative, Lived experience, Historical narrative, Treaty narrative, Scientific narrative, and Planning narrative.</li>
            <li>Connect your narrative to one or more kaitiaki <a href="#" @click="scrollToUserManualSection('Atua')">Atua</a>. Atua options are Rūaumoko, Tangaroa, Tāne, Tāwhirimātea, Tūmatauenga, Rongomātāne and Haumietiketike.</li>
            <li>Locate your narrative. (optional) You are asked to draw a rectangle around the area that your narrative takes place to define the spatial extent of it.</li>
            <li>Summary. Summarise your narrative with a brief abstract of the story – who was involved, where it occurred, what happened.</li>
            <li><a href="#" @click="scrollToUserManualSection('AddElementsToYourNarrative')">Add elements to your narrative</a>. Using the button ‘Add element to the story’ you can add text elements, upload media files, draw geometries including points, lines or polygons (areas) or reuse existing geometries on the map into the story in order to give some spatial context to the narrative. Elements added to the narrative can be reordered by dragging and dropping them after clicking the button ‘Drag me’ in the top of each element.</li>
            <li>Press ‘Save story’ to save changes. Accessing My narratives list in the left sidebar, the created narrative will be listed in the top of the list, as the most recent added narrative.</li>
          </ol>
        </div>
      </div>
    </div>
    <div id="DateTheNarrative">
      <h5 class="mb-3">
        Date the narrative
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4">
          <ul class="user-manual-p">
            <li><b>Precise date:</b> If you know the precise date of your narrative.</li>
            <li><b>Precise year:</b> If you do not know the precise date but know the exact year of your narrative.</li>
            <li><b>Year range:</b> If you do not know the exact year of your narrative or your narrative covers a number of years, select two years between which you know the narrative occurred.</li>
            <li><b>Ancient:</b> If your narrative has no recorded date or is timeless select this option.</li>
          </ul>
        </div>
      </div>
    </div>
    <div id="NarrativeType">
      <h5 class="mb-3">
        Narrative Type
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          Select one or more of the types of narrative below which best categorises your story. This assists people searching and learning about Ōhinemutu.
          <ul class="mt-2">
            <li>
              <b>Traditional narrative:</b> Traditional narratives are tribal stories that have been passed down from ancient times involving legendary ancestors and deeds.
            </li>
            <li>
              <b>Lived experience:</b> Lived experiences are lessons from life, learned from both good and bad experiences, highlight events if you like. These are stories told by the person who experienced the event themselves or it was a story relayed to them by someone who had experienced the event.
            </li>
            <li>
              <b>Historical narrative:</b> Historical narratives about the community are both those that have been passed down orally as well as those documented. Narratives may be held in peoples’ memories, in diaries, photographs, film, books and art works of those in the community.
            </li>
            <li>
              <b>Treaty narrative:</b> Treaty narratives document Treaty of Waitangi outcomes and processes. Outcomes include cultural redress, statutory acknowledgements, deeds of recognition, partnership agreements and co-governance arrangements. Stories about the Treaty from those that were involved in the process can be shared here.
            </li>
            <li>
              <b>Scientific narrative:</b> Scientific narratives are contained in abstracts with link to full articles. There may be a cost to view or download full articles. Commentaries by users on these articles can also be classified within this category.
            </li>
            <li>
              <b>Planning narrative:</b> Planning narratives to support
              <ul>
                <li>Regional and local government plans</li>
                <li>Partnership agreements between iwi or hapū groups and councils</li>
                <li>Outside planning decisions about Ōhinemutu, and the effect of these plans and decisions on the village.</li>
                <li>Iwi management plans.</li>
                <li>Plans prepared at the village level which have been developed by Ōhinemutu residents themselves or other agencies on their behalf.</li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div id="Atua">
      <h5 class="mb-3">
        Atua and Types of Narratives
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4">
          <div class="col-md-2 text-center">
            <img class="atua-img" src="static/img/user_manual/tangaroa.png">
          </div>
          <div class="col-md-10">
            <p class="mb-0">
              <b>Tangaroa</b> is Atua of oceans and inland waterways. Types of Tangaroa narratives include those around:
              <ul>
                <li>
                  Fish, kaimoana, fishing activities
                </li>
                <li>
                  Water quality, water flow
                </li>
              </ul>
            </p>
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-2 text-center">
            <img class="atua-img" src="static/img/user_manual/tane.png">
          </div>
          <div class="col-md-10">
            <p class="mb-0">
              <b>Tāne-mahuta</b> is Atua of forests and birds, and is the fertility force. Tāne is the fertility force and also holds the realm of the day. Types of Tāne narratives include those around:
              <ul>
                <li>
                  Birds - health, harvest
                </li>
                <li>
                  Forests - trees, health, harvest
                </li>
              </ul>
            </p>
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-2 text-center">
            <img class="atua-img" src="static/img/user_manual/tawhirimatea.png">
          </div>
          <div class="col-md-10">
            <p class="mb-0">
              <b>Tāwhirimātea</b> is Atua of the winds and storms. Weather and climate are issues of his domain. Types of Tāwhirimātea narratives include those around:
              <ul>
                <li>
                  Droughts, Rainfall, Floods, Storms
                </li>
                <li>
                  Winds, Temperature
                </li>
                <li>
                  Climate change
                </li>
              </ul>
            </p>
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-2 text-center">
            <img class="atua-img" src="static/img/user_manual/rongo.png">
          </div>
          <div class="col-md-10">
            <p class="mb-0">
              <b>Rongomātāne</b> is Atua of agriculture and peace. Types of Rongo narratives include those around:
              <ul>
                <li>
                  Agriculture, productivity
                </li>
                <li>
                  Surrounding land use
                </li>
                <li>
                  Soils
                </li>
                <li>
                  Rongoa – medicinal plants
                </li>
                <li>
                  Kotahitanga (unity, collective action, holism)
                </li>
              </ul>
            </p>
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-2 text-center">
            <img class="atua-img" src="static/img/user_manual/haumietiketike.png">
          </div>
          <div class="col-md-10">
            <p class="mb-0">
              <b>Haumietiketike</b> is Atua of fern root and wild foods. Types of Haumie narratives include those around:
              <ul>
                <li>
                  Rongoa – medical plants
                </li>
                <li>
                  Hunting – fish, birds, animals
                </li>
                <li>
                  Gathering wild materials – harakeke etc.
                </li>
              </ul>
            </p>
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-2 text-center">
            <img class="atua-img" src="static/img/user_manual/ruaumoko.png">
          </div>
          <div class="col-md-10">
            <p class="mb-0">
              <b>Rūaumoko</b> is the unborn, Atua of earthquakes, volcanoes and other geological phenomena. Types of Rūaumoko narratives include those around:
              <ul>
                <li>
                  Geothermal
                </li>
                <li>
                  Earthquakes
                </li>
                <li>
                  Volcanoes
                </li>
                <li>
                  Gravels, soils, stone
                </li>
              </ul>
            </p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-2 text-center">
            <img class="atua-img" src="static/img/user_manual/tumatauenga.png">
          </div>
          <div class="col-md-10">
            <p class="mb-0">
              <b>Tūmatauenga</b> is Atua of people and war. His issues are political and social. Types of Tū narratives include those around:
              <ul>
                <li>
                  Tino rangatiratanga – self determination
                </li>
                <li>
                  Kaitiakitanga – guardianship
                </li>
                <li>
                  Whanaungatanga – kinship
                </li>
                <li>
                  Manaakitanga – hospitality
                </li>
                <li>
                  Tikanga – customs
                </li>
                <li>
                  Kawa – location based protocols
                </li>
                <li>
                  Economic concerns
                </li>
                <li>
                  Recreation activities
                </li>
              </ul>
            </p>
          </div>
        </div>
      </div>
    </div> <!-- atua div ends -->
    <div id="AddElementsToYourNarrative">
      <h5 class="mb-3">
        Add elements to your narrative
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          Your narratives can be made up of text and media files (including photos, video and audio). You can also add links to other documents and files. To add new elements to a narrative, use the button ‘Add element to the story’ to open the options popup, as shown below.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/addElementToStory.png">
        </div>
        <div class="row mb-4 user-manual-p">
          Clicking the ‘New Text field’ option, a new text area appears in which you can write and add some style to the text, as shown below.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/addtext.png">
        </div>
        <div class="row mb-4 user-manual-p">
          Clicking the ‘Upload Media file’ option inside the ‘Add element to the story’ popup, the Upload File popup appears requesting you to click in the dashed area to browse the media file in your file system or to drop the select file in the area by dragging it from the folder in file system. After adding the file, the upload progress in displayed in percentage and when the upload has finished, the name of the file is displayed in that area. While the file is being uploaded, you can write a little description or caption that will be displayed below the media.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/uploadmediafile.png">
        </div>
        <div class="row mb-4 user-manual-p">
          Finally, pressing ‘Add media to story’ the media is displayed in the right panel, at the top of the added elements, as shown below.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/addmediatostory.png">
        </div>
        <div class="row mb-4 user-manual-p">
          Clicking the ‘Draw map geometry’ option inside the ‘Add element to the story’ popup, the map drawing interaction activates and the drawing buttons appear along the left margin of the map. Through this functionality, you can add locations to your narrative as points, lines (several points in a row) or polygons (areas) about which a narrative is told of that place or places. This provides spatial context to the narrative and allows you to locate and display your narrative on the map for easy visualisation and retrieval.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/drawmapgeometry.png">
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/addpointcoordinate.png">
          <span class="col-md-10"><strong>Add point coordinate - </strong>
            Insert coordinates in decimal degrees or ‘get my location’ to locate your narrative in the location you are currently in (the application gets the coordinates of your present location).
          </span>
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/drawpoint.png">
          <span class="col-md-10"><strong>Draw point - </strong>
            Create a point to locate your narrative about a single place or geographic feature.
          </span>
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/drawline.png">
          <span class="col-md-10"><strong>Draw line - </strong>
            Create a series of points to locate your narrative along a line.
          </span>
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/drawpolygon.png">
          <span class="col-md-10"><strong>Draw polygon - </strong>
            Create an area to locate your narrative about a single place or geographic feature.
          </span>
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/stopdrawing.png">
          <span class="col-md-10"><strong>Stop drawing geometry - </strong>
            Exit the  Map drawing interaction.
          </span>
        </div>
        <div class="row mb-4 user-manual-p">
          After selecting one of the geometry types by clicking on one of the buttons displayed above, you can start clicking on the map to draw your geometry. If you selected Point geometry, once you click on the map (in the location you want to draw the point) the geometry is finalised showing a panel that slides from the bottom of the map where you can add some information about what you draw. If you draw a Line or a Polygon, you must finalise the drawing double-clicking, and the information panel slides up from the bottom of the map. The drawn geometry is in yellow.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/storyfeatureinfo.png">
        </div>
        <div class="row mb-4 user-manual-p">
          You can change the drawing shape by snapping the cursor over the drawing and dragging the blue dot which is displayed. After writing some details about what is drawn, click on ‘Add feature to story’ in order to save the geometry in the narrative, and the new drawn location appears in the top of the story elements in the right panel, as shown below.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/addfeaturetostory.png">
        </div>
        <div class="row mb-4 user-manual-p">
          When saving the geometry, the geometry information panel closes, the map drawing interaction stops and the drawn geometry turns blue (the yellow colour indicates that the geometry is being edited). The geometry detail appears in the top of the story elements in the right side panel, as shown above with the red rectangle. From this new geometry element in the story you can, at any time, click in these four buttons to perform actions on the specific drawn geometry:
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/zoomtogeometry.png">
          <span class="col-md-10"><strong>Zoom to geometry - </strong>
            zoom to the drawn location
          </span>
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/editgeometry.png">
          <span class="col-md-10"><strong>Edit geometry - </strong>
            change the geometry’s details and shape
          </span>
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/editgeometrystyle.png">
          <span class="col-md-10"><strong>Edit geometry style - </strong>
            change its style including colour, line width and opacity
          </span>
        </div>
        <div class="mb-4">
          <img class="atua-img" src="static/img/user_manual/managemediageometry.png">
          <span class="col-md-10"><strong>Manage media about the geometry - </strong>
            add/remove media about the specific location
          </span>
        </div>
        <div class="row mb-4 user-manual-p">
          The geometries can be created by you or reused from other layers or narratives created by others. For the latter, you just need to click ‘Reuse map geometry’ inside the ‘Add element to the story’ popup, and then click in any existing geometry on the map to identify the geometry you would like to duplicate into your narrative.
        </div>
      </div>
    </div><!-- AddElementsToYourNarrative div ends -->
    <div id="CoCreateStory">
      <h5 class="mb-3">
        Co-create a narrative
      </h5>
      <div class="user-manual-content">
        <div class="mb-4 user-manual-p">
          Your narrative may be created by yourself alone or a number of other co-authors. Perhaps you only know part of a story or another member has creative skills that they can offer to enhance the story. You can invite other members as co-authors to contribute to a story through the Co-create narrative functionality. After saving your narrative, invite other members as co-authors to contribute to your story. For that, you just need to click in the  <img class="user-manual-inline-image" src="static/img/user_manual/cocreatestorybutton.png"> dropup button in the footer of the story panel and then click in ‘Co-create narrative’ to open the invite co-creator modal.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/cocreatestory.png">
        </div>
        <div class="row mb-4 user-manual-p">
          Then just type the username of the person you want to invite and, as you type, the autocompleting helps you to complete the username you are writing. When the username you are looking for appears in the list, just click on it and the person is now a co-creator since you are granting editing permissions to this person. If no suggestion appears it is because there is no user with that specified username.
        </div>
      </div>
    </div>
    <div id="PublishNarrative">
      <h5 class="mb-3">
        Submit and Publish your narrative
      </h5>
      <div class="user-manual-content">
        <div class="mb-4 user-manual-p">
          Once you have finished your story you may want to publish your story to a Kōhanga nest. Once published to a nest, then all other members of that nest will be able to read and comment on your narrative. In order to publish the narrative you must first submit the narrative for validation to the kaitiaki of the nest you wish to make the narrative available. To submit the narrative click in the  <img class="user-manual-inline-image" src="static/img/user_manual/cocreatestorybutton.png"> dropup button in the footer of the story panel and then click in ‘Submit narrative’ to open the Submit narrative modal. At this point you will be asked to determine the kōhanga nest that you think are most appropriate to publish into. Options are whanau, koro matua, Ngāti Whakaue or Tātou.
        </div>
      </div>
    </div>
    <div id="KohangaNests">
      <h5 class="mb-3">
        Kōhanga nests
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          What Kōhanga nest that you think your narrative is most appropriate to be shared with; Whanau, Koromātua, Ngāti Whakaue or Tātou? See Kōhanga nest diagram below. Your narrative will be submitted to the appropriate mandated kaitiaki to validate or recommend further work. in the footer of the story panel and then click in ‘Submit narrative’ to open the Submit narrative modal. At this point you will be asked to determine the kōhanga nest that you think are most appropriate to publish into. Options are whanau, koro matua, Ngāti Whakaue or Tātou.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/nests.png">
        </div>
        <ul class="user-manual-p">
          <li>
            <strong>Whanau nest</strong> - These are stories that are most appropriate to share within your whanau. Members of your whanau will be able to make comments on your story. This nest does not require validation for a story to be published, you just publish it directly to your whanau.
          </li>
          <li>
            <strong>Koromātua nest</strong> - These are stories which are appropriate to share to members within one or more koromātua o Ngāti Whakaue, these being Te Rorooterangi, Tunuhopu, Taeotu, Te Rangiiwaho, Pukaki and Hurungaterangi. They are approved and published by one or more kaitiaki mandated by their koromātua.
          </li>
          <li>
            <strong>Ngāti Whakaue nest</strong> - These are stories that you think all registered members of Ngāti Whakaue would be interested in. They will be approved by the ODWG Incorporated Society.
          </li>
          <li>
            <strong>Tātou nest</strong> - These are stories that you think would be of interest to the public about Ōhinemutu.  They may already in the public domain or are specifically developed to provide information by ODWG Incorporated Society about the village to the public. Those people who whakapapa to Ngāti Whakaue who are not registered members would be able to access some narratives about their whānui.
          </li>
        </ul>
      </div>
    </div>
    <div id="NarrativeSubmissionWorkflow">
      <h5 class="mb-3">
        Narrative submission workflow
      </h5>
      <div class="user-manual-content">
        <div class="row mb-4 user-manual-p">
          After selecting the Kōhanga nest, press Submit. Your narrative is then sent to the respective kaitiaki to validate it. If you are submitting a narrative to your whanau there is no validation process, however, inappropriate or vexatious narratives can be removed or moderated by the Administrator.  The kaitiaki will either accept the narrative, as is, or reply to the authors with feedback to improve the narrative before publication. Through this process the status of the narrative changes from DRAFT, SUBMITTED, ACCEPTED to PUBLISHED.
        </div>
        <div class="row mb-4 user-manual-p">
          Below is a flow chart of the process of publishing your narrative depending on the nest you are publishing to, followed by explanations of the steps.
        </div>
        <div class="row mb-4">
          <img class="user-manual-screenshot-img" src="static/img/user_manual/submissionworkflow.png">
        </div>
        <ul class="user-manual-p">
          <li>
            <strong>Save narrative</strong> - At first the status of your narrative is 'DRAFT'. These are narratives that are not published. They just stay with you, the creator or creators of the story, until you are ready to share or not. When you and your co-creator(s) are satisfied your narrative is completed the lead author  submits the narrative to an appropriate kōhanga nest through the button 'Submit narrative'. Options are whanau, koromātua, Ngāti Whakaue or Tātou. See <a href="#" @click="scrollToUserManualSection('KohangaNests')">Kōhanga nest diagram</a> and description.
          </li>
          <li>
            <strong>Submit narrative</strong> - If your narrative is submitted to your whanau, the narrative's status passes from 'DRAFT' to 'PUBLISHED' directly as there is no requirement for third-party kaitiaki validation in this situation. Note: If a story is felt to be untrue, offensive or otherwise inappropriate an affected whanau member can use the <img class="user-manual-inline-image" src="static/img/user_manual/blowhorn.jpg">button requesting the administrator to have the narrative removed or moderated. If your narrative is submitted to a koromātua, Ngāti Whakaue or a tātou nest the narrative gets the status 'SUBMITTED' and is sent to a mandated third-party kaitiaki for validation.
          </li>
          <li>
            <strong>Accept narrative</strong> - If the kaitiaki feels that your narrative requires further work they will send a validation review to you and your co-creators with suggestions for completion. If the kaitiaki feels that the narrative is complete, the narrative's status becomes 'ACCEPTED'. Only with this status the button 'Publish narrative' becomes available to the lead author.
          </li>
          <li>
            <strong>Publish narrative</strong> - For the koromātua, Ngāti Whakaue and tātou nests, when the narrative’s status becomes ‘ACCEPTED’ then the co-creators are notified. The lead author is then is able to press the button 'Publish narrative'. The narrative gets the status 'PUBLISHED'.
            After a narrative is 'PUBLISHED', if a co-creator re-edits the story and saves the changes, the narratives gets again the status 'DRAFT' (so it's not published anymore) and it will need to be submitted again for the mandated kaitiaki's validation.
          </li>
          <li>
            <strong>Unpublish narrative</strong> - With the ’PUBLISHED’ status the button 'Unpublish narrative' becomes available (in case the co-creator wants to unpublish). If the co-creator unpublishes the narrative, it gets again the status 'ACCEPTED' and the button 'Publish narrative' becomes available once again.
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  // data() {
  //   return {
  //     section: null
  //   }
  // },
  computed: {
    userManualSection () {
      return this.$store.state.userManualSection
    }
  },
  methods: {
    scrollToUserManualSection (content) {
      this.$store.commit('SET_USER_MANUAL_SECTION', content)
      //$('#userManualModal').modal('show')
      setTimeout(function(){
        var element = document.querySelector('#' + content);
        element.scrollIntoView({ behavior: 'smooth', block: 'start'});
      },500);
    },
  }
}
</script>
