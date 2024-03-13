# WOW! A file with no Python Imports?
# Third Party Imports
from interactions import Modal, ParagraphText, ShortText

# What will these classes do?
# Make my life less painful
# by making building Modals easier.

# BIG LIMIT: MODALS CAN ONLY HAVE 5 COMPONENTS

# Go Builder Class!
# We will be using Builder Pattern!
# A simple class
class ModalBuilder:
    """Builds Modals (those forms in discord) for taking user inputs.
    \n\nThis class will build two types of Modals to be sent, which are named appropriately, these are:
    \n\n\t1. Modal for Embed Building: CustomEmbedInfo
    \n\t2. Modal for Text Message Building: CustomTextInfo
    \n\t3. Modal for Field Building for Embeds: CustomFieldsInfo
    \n\nParameters:
    \n\n\t1. ModalTitle: str, The `title` of the Modal\n\n
    \n\t2. ModalCustomID: str, The `custom_id` of the Modal, this will be used later to read those inputs\n"""
    
    def __init__(self, ModalTitle: str, ModalCustomID: str)-> None:
        self.modal_title = ModalTitle
        self.modal_custom_id = ModalCustomID

        # Since, Modal can accept components(InputText or ParagraphText or ShortText) as a list
        # we will be making it as a list, so we can append based on bool values.
        self.components = []

    # Modal for Embed Building
    def CustomEmbedInfo(
            self,
            get_embed_title: bool = False,
            get_embed_description: bool = False,
            get_embed_ephemeral: bool = False
    ) -> Modal:
        """A very simple method (or is it), you just need to decide True/False values\
        for some of the parameters and it will build it for you!\n\n
        Parameters (and what they will do):\n\n\
        1. `get_embed_title`: By default a False value. When enabled, it will add a `ParagraphText`\
component to the Modal (aka those big blanks in the form, those with 4000 word limit). You can read this value to get `title` 
        value for an Embed.\n
        2. `get_embed_description`: By default a False value. When enabled, it will add a `ParagraphText`\
component to the Modal (yes those big blanks with 4000 word limit). You can read this value to get `description` 
        value for an Embed.\n
        3. `get_embed_ephemeral`: By default a False value. When changed to some positive int, it will add a `ShortText` component\
to the Modal (aka those tiny boxes). You can read this value to ger `ephemeral` for an Embed.\n
        \nThese are for the `name` of the field its `value`. Read these two components to get the `name` and `value` for an Embed Field"""
        
        self.components = []  # let's ensure that this thing is empty

        if get_embed_title:     # Appending ParagraphText if True
            self.components.append(
            ParagraphText(
                label="Embed title",
                placeholder="Remember! Markdowns don't work in titles!",
                required=False,
                custom_id="get_embed_title"
            )
        )
            
        if get_embed_description:   # Appending ParagraphText if True
            self.components.append(
            ParagraphText(
                label="Embed Description!",
                placeholder="Markdowns work here! :D",
                required=False,
                custom_id="get_embed_description"
            )
        )
        
        if get_embed_ephemeral:     # Appending ShortText if True
            self.components.append(
                ShortText(
                    label="Hidden?",
                    placeholder="Should the Embed be hidden or not? True or False",
                    required=True,
                    max_length=5,
                    custom_id="get_embed_ephemeral"
                )
            )
        """
        # smh smh my head
        if no_of_fields < 0:
            raise ValueError(
                "ShadowsLure: You had one job, to not play with the negatives, yet you did. "
                "Please consider to refrain from being a math nerd and use positive values only! Thanks!"
            )
        """
        
        return Modal(*self.components, title=self.modal_title, custom_id=self.modal_custom_id)
    
    # Modal for Text Message Building
    def CustomTextInfo(
            self,
            get_ephemeral: bool = False
    )->Modal:
        """A very simple method (really), you will need to decide bool value for one parameter:\n\n\
        \t1. `get_ephemeral`: By default False. When set to True, it will add a `ParagraphText` component to the Modal.
        You can read this value to get `ephemeral` value for `send`."""
        
        self.components = [] # yes, I said empty

        # Let's by default append one ParagraphText for input
        self.components.append(
            ParagraphText(
                label="What would you like to send?",
                placeholder="All Discord Markdowns work! Happy customizing!"
            )
        )

        if get_ephemeral:   # Append if True
            self.components.append(
                ShortText(
                    label="Hidden?",
                    placeholder="Should the Embed be hidden or not? True or False",
                    required=True
                )
            )
        return Modal(*self.components, title=self.modal_title, custom_id=self.modal_custom_id)
    
    def CustomFieldsInfo(
            self
    )-> Modal:
        
        self.components = []  # ensuring a void

        self.components.extend((
            ShortText(
                label="Field Name",
                placeholder="Markdowns don't work here!",
                required=False
            ),
            ParagraphText(
                label="Field Value",
                placeholder="Markdowns don't work here!",
                required=False
            ),
            ShortText(
                label="Inline?",
                placeholder="True or False",
                required=True,
                max_length=5
            )
        ))

        return Modal(*self.components, title = self.modal_title, custom_id=self.modal_custom_id)
        