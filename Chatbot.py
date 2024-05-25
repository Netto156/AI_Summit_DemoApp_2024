from openai import OpenAI
import streamlit as st
import re
import time
from email.message import EmailMessage
import smtplib
from streamlit_extras.stylable_container import stylable_container
import os
from supabase import create_client, Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# python -m streamlit run Chatbot.py


# Set constants
MODEL_ID = st.secrets["model_id"]
API_KEY = st.secrets["api_key"]
RUN_MODE = st.secrets["run_mode"]
NAME_DB = st.secrets["db_name"]


EMAIL_TEMPLATE = ["""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml" lang="en"><head>
    <title>Thank you for trying Hypee</title>
    <meta property="og:title" content="Thank you for trying Hypee">
    <meta name="twitter:title" content="Thank you for trying Hypee">
    
    
    
<meta name="x-apple-disable-message-reformatting">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<meta http-equiv="X-UA-Compatible" content="IE=edge">

<meta name="viewport" content="width=device-width, initial-scale=1.0">


    <!--[if gte mso 9]>
  <xml>
      <o:OfficeDocumentSettings>
      <o:AllowPNG/>
      <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
  </xml>
  
  <style>
    ul > li {
      text-indent: -1em;
    }
  </style>
<![endif]-->
<!--[if mso]>
<style type="text/css">
 body, td {font-family: Arial, Helvetica, sans-serif;}
 .hse-body-wrapper-table {background-color: #f2f2f2;}
</style>
<![endif]-->


  <base href="https://1926778.hubspotpreview-na1.com/content-rendering/v1/public/_hcms/preview/email/167461289252?portalId=1926778&amp;preview_key=pGakUysr&amp;_preview=true&amp;from_buffer=true&amp;cacheBust=1716282683604&amp;hsPreviewerApp=email" target="_blank"><meta name="generator" content="HubSpot"><meta property="og:url" content="https://info.incentro.com/-temporary-slug-e4bc002f-53d4-47dc-8e2d-4969c8f3863c?hs_preview=pGakUysr-167461289252"><meta name="robots" content="noindex,follow"><!--[if !((mso)|(IE))]><!-- --><style type="text/css">.moz-text-html .hse-column-container{max-width:600px !important;width:600px !important}
.moz-text-html .hse-column{display:table-cell;vertical-align:top}.moz-text-html .hse-section .hse-size-4{max-width:200px !important;width:200px !important}
.moz-text-html .hse-section .hse-size-8{max-width:400px !important;width:400px !important}
.moz-text-html .hse-section .hse-size-12{max-width:600px !important;width:600px !important}
@media only screen and (min-width:640px){.hse-column-container{max-width:600px !important;width:600px !important}
.hse-column{display:table-cell;vertical-align:top}.hse-section .hse-size-4{max-width:200px !important;width:200px !important}
.hse-section .hse-size-8{max-width:400px !important;width:400px !important}.hse-section .hse-size-12{max-width:600px !important;width:600px !important}
}@media only screen and (max-width:639px){img.stretch-on-mobile,.hs_rss_email_entries_table img,.hs-stretch-cta .hs-cta-img{height:auto !important;width:100% !important}
.display_block_on_small_screens{display:block}.hs_padded{padding-left:20px !important;padding-right:20px !important}
.hs-hm,table.hs-hm{display:none}.hs-hd{display:block !important}table.hs-hd{display:table !important}
}@media screen and (max-width:639px){.social-network-cell{display:inline-block} }</style><!--<![endif]--><style type="text/css">#hs_body #hs_cos_wrapper_main a[x-apple-data-detectors]{color:inherit !important;text-decoration:none !important;font-size:inherit !important;font-family:inherit !important;font-weight:inherit !important;line-height:inherit !important}
a{text-decoration:underline}p{margin:0}body{-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%;-webkit-font-smoothing:antialiased;moz-osx-font-smoothing:grayscale}</style></head>
  <body id="hs_body" bgcolor="#f2f2f2" style="margin:0 !important; padding:0 !important; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word">
    <div id="preview_text" style="display:none;font-size:1px;color:#f2f2f2;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;" lang="en">Here are your results!</div>
    
<!--[if gte mso 9]>
<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
    <v:fill type="tile" size="100%,100%" color="#ffffff"/>
</v:background>
<![endif]-->

    <div class="hse-body-background" lang="en" style="background-color:#f2f2f2" bgcolor="#f2f2f2">
      <table role="presentation" class="hse-body-wrapper-table" cellpadding="0" cellspacing="0" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; margin:0; padding:0; width:100% !important; min-width:320px !important; height:100% !important" width="100%" height="100%">
        <tbody><tr>
          <td class="hse-body-wrapper-td" valign="top" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding-top:20px; padding-bottom:20px">
            <div id="hs_cos_wrapper_main" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_dnd_area" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="dnd_area">  
  <div id="section-0" class="hse-section hse-section-first" style="padding-left:10px; padding-right:10px">

    
    
    <!--[if !((mso)|(IE))]><!-- -->
      <div class="hse-column-container" style="min-width:280px; max-width:600px; Margin-left:auto; Margin-right:auto; border-collapse:collapse; border-spacing:0; background-color:#ffffff" bgcolor="#ffffff">
    <!--<![endif]-->
    
    <!--[if (mso)|(IE)]>
      <div class="hse-column-container" style="min-width:280px;max-width:600px;width:100%;Margin-left:auto;Margin-right:auto;border-collapse:collapse;border-spacing:0;">
      <table align="center" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:600px;" cellpadding="0" cellspacing="0" role="presentation" width="600" bgcolor="#ffffff">
      <tr style="background-color:#ffffff;">
    <![endif]-->

    <!--[if (mso)|(IE)]>
  <td valign="top" style="width:600px;">
<![endif]-->
<!--[if gte mso 9]>
  <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:600px">
<![endif]-->
<div id="column-0-0" class="hse-column hse-size-12">
  <div id="hs_cos_wrapper_module-0-0-0" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><table class="hse-image-wrapper" role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt">
  <tbody>
    <tr>
      <td class="hs_padded" align="center" valign="top" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; color:#444444; word-break:break-word; text-align:center; padding:20px 20px 10px; font-size:0px">
        <img alt="Incentro-logo-2018-Orange" src="https://cdn2.hubspot.net/hub/1926778/hubfs/Incentro-logo-2018-Orange.png?width=300&amp;upscale=true&amp;name=Incentro-logo-2018-Orange.png" style="outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; max-width:100%; font-size:16px" width="150" align="middle">
      </td>
    </tr>
  </tbody>
</table></div>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:10px 20px"><div id="hs_cos_wrapper_module-0-0-1" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><table role="none" border="0" cellpadding="0" cellspacing="0" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; vertical-align:top" width="100%">
  <tbody><tr>
    <td align="left" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; color:#444444; font-size:0; word-break:break-word">
      <p style="mso-line-height-rule:exactly; font-size:1px; border-top:2px solid #FE5000; width:100%; margin:0"></p>
      <!--[if mso]>
        <table role="none" align="left" border="0" cellpadding="0" cellspacing="0" style="font-size:1px;border-top:2px solid #FE5000;width:560px;">
          <tr>
            <td style="height:0;line-height:0">&nbsp;</td>
          </tr>
        </table>
      <![endif]-->
    </td>
  </tr>
</tbody></table></div></td></tr></tbody></table>
</div>
<!--[if gte mso 9]></table><![endif]-->
<!--[if (mso)|(IE)]></td><![endif]-->

    <!--[if (mso)|(IE)]></tr></table><![endif]-->

    </div>
   
  </div>
  
  
  <div id="section-1" class="hse-section" style="padding-left:10px; padding-right:10px">

    
    
    <!--[if !((mso)|(IE))]><!-- -->
      <div class="hse-column-container" style="min-width:280px; max-width:600px; Margin-left:auto; Margin-right:auto; border-collapse:collapse; border-spacing:0; background-color:#ffffff" bgcolor="#ffffff">
    <!--<![endif]-->
    
    <!--[if (mso)|(IE)]>
      <div class="hse-column-container" style="min-width:280px;max-width:600px;width:100%;Margin-left:auto;Margin-right:auto;border-collapse:collapse;border-spacing:0;">
      <table align="center" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:600px;" cellpadding="0" cellspacing="0" role="presentation" width="600" bgcolor="#ffffff">
      <tr style="background-color:#ffffff;">
    <![endif]-->

    <!--[if (mso)|(IE)]>
  <td valign="top" style="width:600px;">
<![endif]-->
<!--[if gte mso 9]>
  <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:600px">
<![endif]-->
<div id="column-1-0" class="hse-column hse-size-12">
  <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:10px 20px"><div id="hs_cos_wrapper_module_17157586945721" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><div id="hs_cos_wrapper_module_17157586945721_" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_rich_text" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="rich_text"><h1 style="margin:0; mso-line-height-rule:exactly; line-height:175%; font-family:Arial, sans-serif; font-size:24px"><span style="color: #000000;"><span style="color: #fe5000;">Hypee</span> results incoming!&nbsp;</span></h1></div></div></td></tr></tbody></table>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:20px"><div id="hs_cos_wrapper_module-1-0-1" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><div id="hs_cos_wrapper_module-1-0-1_" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_rich_text" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="rich_text"><h2 style="margin:0; mso-line-height-rule:exactly; font-size:15px; line-height:125%"><span style="font-family: Helvetica, Arial, sans-serif; color: #000000;">Hi  
""", 
"""
</span><span style="font-family: Helvetica, Arial, sans-serif;">,</span></h2>
<p style="mso-line-height-rule:exactly; line-height:175%">&nbsp;</p>
<p style="mso-line-height-rule:exactly; line-height:175%"><span style="color: #000000;">Thank you for trying out Hypee! Below, you'll find the details of your conversation. I hope it has sparked some inspiration on how you could leverage hyperautomation solutions within your organization.</span></p>
<p style="mso-line-height-rule:exactly; line-height:175%">&nbsp;</p>
<p style="mso-line-height-rule:exactly; line-height:175%"><span style="color: #000000;">Even though we are very fond of Hypee, discovering the full automation potential is currently a bridge too far. That's why we continue to perform our Hyperautomation Scan with the expertise of our human consultants. Learn more about this effective method for uncovering use cases and gaining valuable insights <a href="https://www.incentro.com/en/hyperautomation/win-a-hyperautomation-scan" rel="noopener" style="color:#00a4bd; mso-line-height-rule:exactly" data-hs-link-id="0" target="_blank">here</a>. Or plan a one-on-one with me—I’m more than happy to tell you all the details.</span></p></div></div></td></tr></tbody></table>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:10px 20px"><div id="hs_cos_wrapper_module_17157587243892" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><table align="left" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-spacing:0 !important; mso-table-lspace:0pt; mso-table-rspace:0pt; border-collapse:separate!important">
    <tbody><tr><!--[if mso]>
          <td align="center" valign="middle" bgcolor="#FE5000" style="border-radius:20px;cursor:auto;background-color:#FE5000;padding:12px 18px">
        <![endif]-->
        <!--[if !mso]><!-- -->
          <td align="center" valign="middle" bgcolor="#FE5000" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; border-radius:20px; cursor:auto; background-color:#FE5000">
        <!--<![endif]--><a href="https://meetings.hubspot.com/sacha-vanessen/inspiratiesessie-automation" target="_blank" style="color:#00a4bd; mso-line-height-rule:exactly; font-size:14px; font-family:Arial, sans-serif; Margin:0; text-transform:none; text-decoration:none; padding:12px 18px; display:block" data-hs-link-id="0">
          <strong style="color:#ffffff;font-weight:bold;text-decoration:none;font-style:normal;">Book an appointment</strong>
        </a>
      </td>
    </tr>
  </tbody></table></div></td></tr></tbody></table>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:10px 20px"><div id="hs_cos_wrapper_module_17157588133725" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><table role="none" border="0" cellpadding="0" cellspacing="0" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; vertical-align:top" width="100%">
  <tbody><tr>
    <td align="center" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; color:#444444; font-size:0; word-break:break-word">
      <p style="mso-line-height-rule:exactly; font-size:1px; border-top:1px solid #FE5000; width:100%; margin:0 auto"></p>
      <!--[if mso]>
        <table role="none" align="center" border="0" cellpadding="0" cellspacing="0" style="font-size:1px;border-top:1px solid #FE5000;width:560px;">
          <tr>
            <td style="height:0;line-height:0">&nbsp;</td>
          </tr>
        </table>
      <![endif]-->
    </td>
  </tr>
</tbody></table></div></td></tr></tbody></table>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:10px 20px"><div id="hs_cos_wrapper_module_17162810339241" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><div id="hs_cos_wrapper_module_17162810339241_" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_rich_text" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="rich_text"><h2 style="margin:0; mso-line-height-rule:exactly; font-size:20px; line-height:175%"><span style="color: #000000;">Your Hypee results</span></h2></div></div></td></tr></tbody></table>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt">
    <!-- Input results below -->
""",
"""
 <!-- Input results above -->               
</table>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:10px 20px"><div id="hs_cos_wrapper_module_17162810626362" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><table role="none" border="0" cellpadding="0" cellspacing="0" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; vertical-align:top" width="100%">
  <tbody><tr>
    <td align="center" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; color:#444444; font-size:0; word-break:break-word">
      <p style="mso-line-height-rule:exactly; font-size:1px; border-top:1px solid #FE5000; width:100%; margin:0 auto"></p>
      <!--[if mso]>
        <table role="none" align="center" border="0" cellpadding="0" cellspacing="0" style="font-size:1px;border-top:1px solid #FE5000;width:560px;">
          <tr>
            <td style="height:0;line-height:0">&nbsp;</td>
          </tr>
        </table>
      <![endif]-->
    </td>
  </tr>
</tbody></table></div></td></tr></tbody></table>
</div>
<!--[if gte mso 9]></table><![endif]-->
<!--[if (mso)|(IE)]></td><![endif]-->

    <!--[if (mso)|(IE)]></tr></table><![endif]-->

    </div>
   
  </div>

  <div id="section_17157588044314" class="hse-section" style="padding-left:10px; padding-right:10px">

    <!--[if !((mso)|(IE))]><!-- -->
      <div class="hse-column-container" style="min-width:280px; max-width:600px; Margin-left:auto; Margin-right:auto; border-collapse:collapse; border-spacing:0; background-color:#ffffff" bgcolor="#ffffff">
    <!--<![endif]-->
    
    <!--[if (mso)|(IE)]>
      <div class="hse-column-container" style="min-width:280px;max-width:600px;width:100%;Margin-left:auto;Margin-right:auto;border-collapse:collapse;border-spacing:0;">
      <table align="center" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:600px;" cellpadding="0" cellspacing="0" role="presentation" width="600" bgcolor="#ffffff">
      <tr style="background-color:#ffffff;">
    <![endif]-->

    <!--[if (mso)|(IE)]>
  <td valign="top" style="width:400px;">
<![endif]-->
<!--[if gte mso 9]>
  <table role="presentation" width="400" cellpadding="0" cellspacing="0" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:400px">
<![endif]-->
<div id="column-1715758804431-0" class="hse-column hse-size-8">
  <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:20px"><div id="hs_cos_wrapper_module_17157588044312" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><div id="hs_cos_wrapper_module_17157588044312_" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_rich_text" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="rich_text"><div style="mso-line-height-rule:exactly; font-size:14px; line-height:150%"><span style="color: #000000;"><strong>Warm regards, </strong></span></div>
<div style="mso-line-height-rule:exactly; font-size:14px; line-height:150%">&nbsp;</div>
<div style="mso-line-height-rule:exactly; font-size:14px; line-height:150%"><span style="color: #000000;"><strong>Sacha van Essen</strong></span></div>
<p style="mso-line-height-rule:exactly; font-size:14px; line-height:150%">&nbsp;</p>
<p style="mso-line-height-rule:exactly; font-size:14px; line-height:150%">&nbsp;</p>
<p style="mso-line-height-rule:exactly; font-size:14px; line-height:150%"><span style="font-weight: bold; color: #000000;">e: </span><span style="color: #fe5000;"><a href="mailto:sacha.vanessen@incentro.com" style="mso-line-height-rule:exactly; color:#fe5000; text-decoration:underline; font-weight:bold" rel="noopener" data-hs-link-id="0" target="_blank">sacha.vanessen@incentro.com</a></span></p>
<p style="mso-line-height-rule:exactly; font-size:14px; line-height:150%"><span style="color: #000000;"><span style="font-weight: bold;">t: </span><span style="font-weight: normal;">+316 22912560</span></span></p></div></div></td></tr></tbody></table>
</div>
<!--[if gte mso 9]></table><![endif]-->
<!--[if (mso)|(IE)]></td><![endif]-->
<!--[if (mso)|(IE)]>
  <td valign="top" style="width:200px;">
<![endif]-->
<!--[if gte mso 9]>
  <table role="presentation" width="200" cellpadding="0" cellspacing="0" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:200px">
<![endif]-->
<div id="column-1715758804431-1" class="hse-column hse-size-4">
  <div id="hs_cos_wrapper_module_17157588044313" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><table class="hse-image-wrapper" role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt">
  <tbody>
    <tr>
      <td class="hs_padded" align="center" valign="top" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; color:#444444; word-break:break-word; text-align:center; padding:20px; font-size:0px">
        <a href="https://meetings.hubspot.com/sacha-vanessen/inspiratiesessie-automation" target="_blank" style="color:#00a4bd; mso-line-height-rule:exactly" data-hs-link-id="1">
        <img alt="20230317_SACHA-VAN-ESSEN_SQUARE_0001" src="https://cdn2.hubspot.net/hub/1926778/hubfs/20230317_SACHA-VAN-ESSEN_SQUARE_0001.jpg?width=320&amp;upscale=true&amp;name=20230317_SACHA-VAN-ESSEN_SQUARE_0001.jpg" style="outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; border:none; max-width:100%; font-size:16px" width="160" align="middle">
        </a>
      </td>
    </tr>
  </tbody>
</table></div>
</div>
<!--[if gte mso 9]></table><![endif]-->
<!--[if (mso)|(IE)]></td><![endif]-->

    <!--[if (mso)|(IE)]></tr></table><![endif]-->

    </div>
   
  </div>

  <div id="section-3" class="hse-section hse-section-last" style="padding-left:10px; padding-right:10px">

    <!--[if !((mso)|(IE))]><!-- -->
      <div class="hse-column-container" style="min-width:280px; max-width:600px; Margin-left:auto; Margin-right:auto; border-collapse:collapse; border-spacing:0; background-color:#fe5000; padding-bottom:10px; padding-top:10px" bgcolor="#fe5000">
    <!--<![endif]-->
    
    <!--[if (mso)|(IE)]>
      <div class="hse-column-container" style="min-width:280px;max-width:600px;width:100%;Margin-left:auto;Margin-right:auto;border-collapse:collapse;border-spacing:0;">
      <table align="center" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:600px;" cellpadding="0" cellspacing="0" role="presentation" width="600" bgcolor="#fe5000">
      <tr style="background-color:#fe5000;">
    <![endif]-->

    <!--[if (mso)|(IE)]>
  <td valign="top" style="width:600px;padding-bottom:10px; padding-top:10px;">
<![endif]-->
<!--[if gte mso 9]>
  <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;width:600px">
<![endif]-->
<div id="column-3-0" class="hse-column hse-size-12">
  <div id="hs_cos_wrapper_module-3-0-0" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><table role="presentation" class="hse-footer hse-secondary" width="100%" cellpadding="0" cellspacing="0" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; font-family:Arial, sans-serif; font-size:12px; line-height:135%; color:#23496d; margin-bottom:0; padding:0">
  <tbody>
    <tr>
      <td align="center" valign="top" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; text-align:center; margin-bottom:0; line-height:135%; padding:10px 20px">
        <p style="mso-line-height-rule:exactly; font-family:Helvetica,Arial,sans-serif; font-size:12px; font-weight:bold; text-decoration:none; font-style:normal; color:#ffffff">
          Incentro, Netherlands, Spain, Africa &amp; Bali, Global Digital Solutions
        </p>
        <p style="mso-line-height-rule:exactly">
          <a data-unsubscribe="true" href="https://info.incentro.com/hs/preferences-center/en/direct?data=W2nXS-N30h-FZW4fjRXf3dx1cnW239jbZ1VnLPxW3dynCV30Jcj2W1Qwqbx2vQ3fKW3H3ybP1NxYLjW2TB1ch36CsjdW4crkXG2TtB_2W49QSvW4fGycrW2FVCpD3dgMzmW3BLbdV3SwrkSW38xv-21LCVsRW22TGXJ20WbgvW2TP_0l3zjd-PW211HFF4m8Jp2W47m36L30yL5SW2Kz98M2PNm8wW3bqX6P2MzQhNW217wt72nYcFfW3jgPGv4mq4xyW2-BZGQ383zv_W3QM5fC4tf1vBW2vRKJL2Ft38WW3QStN81N4N0JW2WQcFV2RJsD4W2zwbQq20XQgQW32pbDt3Z_svdW366grg3B_MBwW2p50Tt1XcRC1W4clLyZ2FYzxpW2Wtpgr2qMYH-W2PDWQF3gy61WW41ygY12vNh0WW3P7VX_3T04l70" style="mso-line-height-rule:exactly; font-family:Helvetica,Arial,sans-serif; font-size:12px; color:#FFFFFF; font-weight:normal; text-decoration:none; font-style:normal" data-hs-link-id="0" target="_blank">Unsubscribe</a>
          <a data-unsubscribe="true" href="https://info.incentro.com/hs/preferences-center/en/page?data=W2nXS-N30h-MHW3Hf8XG3XsvNpW1S1qcz30zD1JW2Wp9rR1S32F3W3F8g-72TK1TTW1Zlhc11Z73x5W23jtDd3F50t-W32qt_M45BmyWW32GhDg3g6Dm1W2vPxZN36fhqbW4r696Q49mMV3W3ZxXn04t5x-7W2YHqv41Sz4SGW36lMBb3QDnB6W21hmN01Bnj03W2PxQHj43CVL1W1SfsGz1ZgBzFW2CSMBS3dc3sDW1Vxjmh3JQfTtW3jmlLc1NcrX9W3C15Dk3bzlr4W4pnbY-3FcKLhW32c8P84mH-gKW1Z6fxW3ghPN4W4ppp1j4cP2tBW3P0S5338ynDpW2149vN3_CrlNW3SPPfW2xJNRJW30z-mB3H0gz4W2vPYX52WrFsLW32JP-T36pbCPW1VzRKp1SsmL-W22RHhB1Qmx2fW4cqnnR1X7Lb20" style="mso-line-height-rule:exactly; font-family:Helvetica,Arial,sans-serif; font-size:12px; color:#FFFFFF; font-weight:normal; text-decoration:none; font-style:normal" data-hs-link-id="0" target="_blank">Manage preferences</a>
        </p>
      </td>
    </tr>
  </tbody>
</table></div>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt"><tbody><tr><td class="hs_padded" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:10px 20px"><div id="hs_cos_wrapper_module-3-0-1" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><table role="presentation" align="center" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; width:auto; text-align:center" class="hs_cos_wrapper_type_social_module" width="auto">
  <tbody>
    <tr align="center">
      <td class="social-network-cell" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word">
        <table role="presentation" align="center" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; width:auto; text-align:center" class="hs_cos_wrapper_type_social_module_single" width="auto">
          <tbody>
            <tr align="center">
              <td class="display_block_on_small_screens" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:8px 5px; line-height:1; vertical-align:middle" valign="middle">
                <a href="https://www.linkedin.com/company/21928" style="color:#00a4bd; mso-line-height-rule:exactly; text-decoration:none !important" data-hs-link-id="0" target="_blank">
                    <img src="https://info.incentro.com/hs/hsstatic/TemplateAssets/static-1.262/img/hs_default_template_images/modules/Follow+Me+-+Email/linkedin_original_white.png" alt="LinkedIn" height="40" style="outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; border:none; width:auto!important; height:40px!important; vertical-align:middle" valign="middle" width="auto">
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </td><td class="social-network-cell" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word">
        <table role="presentation" align="center" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; width:auto; text-align:center" class="hs_cos_wrapper_type_social_module_single" width="auto">
          <tbody>
            <tr align="center">
              <td class="display_block_on_small_screens" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:8px 5px; line-height:1; vertical-align:middle" valign="middle">
                <a href="https://twitter.com/IncentroES" style="color:#00a4bd; mso-line-height-rule:exactly; text-decoration:none !important" data-hs-link-id="0" target="_blank">
                    <img src="https://info.incentro.com/hs/hsstatic/TemplateAssets/static-1.262/img/hs_default_template_images/modules/Follow+Me+-+Email/twitter_original_white.png" alt="X" height="40" style="outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; border:none; width:auto!important; height:40px!important; vertical-align:middle" valign="middle" width="auto">
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </td><td class="social-network-cell" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word">
        <table role="presentation" align="center" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; width:auto; text-align:center" class="hs_cos_wrapper_type_social_module_single" width="auto">
          <tbody>
            <tr align="center">
              <td class="display_block_on_small_screens" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:8px 5px; line-height:1; vertical-align:middle" valign="middle">
                <a href="https://www.facebook.com/277658698941469" style="color:#00a4bd; mso-line-height-rule:exactly; text-decoration:none !important" data-hs-link-id="0" target="_blank">
                    <img src="https://info.incentro.com/hs/hsstatic/TemplateAssets/static-1.262/img/hs_default_template_images/modules/Follow+Me+-+Email/facebook_original_white.png" alt="Facebook" height="40" style="outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; border:none; width:auto!important; height:40px!important; vertical-align:middle" valign="middle" width="auto">
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </td><td class="social-network-cell" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word">
        <table role="presentation" align="center" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; width:auto; text-align:center" class="hs_cos_wrapper_type_social_module_single" width="auto">
          <tbody>
            <tr align="center">
              <td class="display_block_on_small_screens" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:8px 5px; line-height:1; vertical-align:middle" valign="middle">
                <a href="https://www.instagram.com/worldofincentro" style="color:#00a4bd; mso-line-height-rule:exactly; text-decoration:none !important" data-hs-link-id="0" target="_blank">
                    <img src="https://info.incentro.com/hs/hsstatic/TemplateAssets/static-1.262/img/hs_default_template_images/modules/Follow+Me+-+Email/instagram_original_white.png" alt="Instagram" height="40" style="outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; border:none; width:auto!important; height:40px!important; vertical-align:middle" valign="middle" width="auto">
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </td><td class="social-network-cell" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word">
        <table role="presentation" align="center" style="border-spacing:0 !important; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; width:auto; text-align:center" class="hs_cos_wrapper_type_social_module_single" width="auto">
          <tbody>
            <tr align="center">
              <td class="display_block_on_small_screens" style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding:8px 5px; line-height:1; vertical-align:middle" valign="middle">
                <a href="https://www.youtube.com/c/Incentro" style="color:#00a4bd; mso-line-height-rule:exactly; text-decoration:none !important" data-hs-link-id="0" target="_blank">
                    <img src="https://info.incentro.com/hs/hsstatic/TemplateAssets/static-1.262/img/hs_default_template_images/modules/Follow+Me+-+Email/youtube_original_white.png" alt="YouTube" height="40" style="outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; border:none; width:auto!important; height:40px!important; vertical-align:middle" valign="middle" width="auto">
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>

</div></td></tr></tbody></table>
</div>
<!--[if gte mso 9]></table><![endif]-->
<!--[if (mso)|(IE)]></td><![endif]-->

    <!--[if (mso)|(IE)]></tr></table><![endif]-->

    </div>
   
  </div>
  </div>
          </td>
        </tr>
      </tbody></table>
    </div>
  
</body></html>
"""]

MAIN_CSS = """ 
    div[data-testid="stFullScreenFrame"] > div {
            justify-content: center;
        }

    div.CenterElem {
        text-align: center;
    }

    div.FormHeader {
        text-align: center;
        font-size: x-large;
        color: #fe5000;
        font-weight: bolder;
        padding:30px;
    }

    h1 {
        text-align: center;
    }

    p {
        font-family: sans-serif;
        font-size: large;
    }

    div[data-testid="stLinkButton"] p {
        font-weight: bolder;
        font-size: medium;
        color: #000;
    }

    div[data-testid="stFormSubmitButton"] button,
     div[data-testid="stLinkButton"] a {
        width: 100%;
    }

    div[data-testid="stFormSubmitButton"] p,
    div[data-testid="stTextInput"] p,
    div[data-testid="stButton"] p,
    div[data-testid="stRadio"] > label p  {
        font-weight: bolder;
        font-size: large;
        color:#000;
    }
    div.PolicyText {
        font-size: x-small;
    }

    div.FormBox{
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 0.5rem;
        padding: calc(1em - 1px);
    }
       
    button[kind="primary"] {
        background-color: #fe5000;
        width:100%;
        border: 2px solid black;
}"""

hide_streamlit_style = """
            <style>
            #MainMenu,
            footer,
            header[data-testid="stHeader"],
            div[class*="viewerBadge_link"]{
                visibility: hidden;    
            }
            div[class*="viewerBadge_link"]:after,
            footer:after {
                content:'goodbye'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 2px;
            }
            </style>
            """
#  ------------------------ Logic ---------------------------------------------
@st.cache_resource
def get_client():
    print("Creating new client....")
    client = OpenAI(api_key=API_KEY)
    return client

CLIENT = get_client()


@st.cache_resource
def connect_to_DB():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    db_connection: Client = create_client(url, key)
    return db_connection

SUPABASE = connect_to_DB()


def insert_into_DB():
    if "sql_record_id" not in st.session_state:
        if "Thread_id" not in st.session_state:
            return
        input_data ={
            "first_name": st.session_state["first_name"],
            "last_name": st.session_state["last_name"],
            "email": st.session_state["email"],
            "liked_demo": None,
            "email_sent": None,
            "thread_id": st.session_state["Thread_id"]
            }
        data, count = SUPABASE.table(NAME_DB).insert(input_data).execute()
        st.session_state["sql_record_id"] = data[1][0]['id']
    else:
        data, count = SUPABASE.table(NAME_DB).upsert({'id': st.session_state["sql_record_id"], 
                                                          'liked_demo':st.session_state["liked"] == "Yes", 
                                                          'email_sent': st.session_state["mail_my_result"] == "Yes"}
                                                          ).execute()


def create_new_thread():
    print("Creating new thread id....")
    thread = CLIENT.beta.threads.create()
    st.session_state['Thread_id'] = thread.id
    return


def validate_user_input():
    data_valid = True

    # Validate email
    if data_valid:
        if not re.match(r"^\S+@\S+\.\S+$", st.session_state['email']):
            data_valid = False

    # Validate first name
    if data_valid:
        data_valid = len(st.session_state['first_name']) >= 2

    # Validate last name
    if data_valid:
        data_valid = len(st.session_state['last_name']) >= 3

    if RUN_MODE == "Debug":
        data_valid=True
        
    # Assign output
    st.session_state['Valid_input'] = data_valid
    return


def query_assistant(user_input):
    assistant=CLIENT.beta.assistants.retrieve(MODEL_ID)
    thread = CLIENT.beta.threads.retrieve(st.session_state['Thread_id'])
    message = CLIENT.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= user_input
    )
    run = CLIENT.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1) # Wait for 1 second
        run = CLIENT.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if run.status == 'completed': 
            messages = CLIENT.beta.threads.messages.list(
            thread_id=thread.id
        )
            GPT_response = messages.data[0].content[0].text.value
        else:
            print(run.status)  
    
    return(GPT_response) 


def mail_conversation():
    if st.session_state["mail_my_result"] == "Yes":
        print("Sending conversation per mail...")

        conversation = fill_mail_template()
        mail_content = "{0}{1}{2}{3}{4}".format(EMAIL_TEMPLATE[0], st.session_state['first_name'], EMAIL_TEMPLATE[1], conversation, EMAIL_TEMPLATE[2])
        send_email(st.session_state['email'], mail_content)
    return


def fill_mail_template():
    result = ""
    for answer in st.session_state['messages']:
        if answer['role'] == 'assistant':
            role = "Hypee"
        else:
            role = st.session_state['first_name']
        result += """<tbody><td style="border-collapse:collapse; mso-line-height-rule:exactly; font-family:Arial, sans-serif; font-size:15px; color:#444444; word-break:break-word; padding-left: 20px; padding-right: 20px; padding-bottom: 15px; padding-top: 15px;"><div id="hs_cos_wrapper_module-1-0-1" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_module" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="module"><div id="hs_cos_wrapper_module-1-0-1_" class="hs_cos_wrapper hs_cos_wrapper_widget hs_cos_wrapper_type_rich_text" style="color: inherit; font-size: inherit; line-height: inherit;" data-hs-cos-general-type="widget" data-hs-cos-type="rich_text"><h2 style="margin:0; mso-line-height-rule:exactly; font-size:15px; line-height:125%"><span style="font-family: Helvetica, Arial, sans-serif; color: #000000;">{0}</span></h2>
    <p style="mso-line-height-rule:exactly; line-height:175%"><span style="color: #000000;">{1}</span></p></div></div></td></tbody>""".format(role, answer['content'])
    return result


def send_email(recipient, message):
    print("sending mail to: "+ recipient)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Recap of conversation with Hypee - UiPath AI Summit"
    msg['From'] = st.secrets["email"]
    msg['To'] = recipient
    content = MIMEText(message, 'html')
    msg.attach(content)

    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls()
        print(st.secrets["email"])
        smtp.login(st.secrets["email"], st.secrets["email_pw"])
        smtp.sendmail(st.secrets["email"], recipient, msg.as_string())
        smtp.quit()

# ---------------------------------- UI Functions --------------------------------------------

def get_user_info():
    print("getting user info")
    st.session_state['Form_count'] += 1
    st.caption(" ")

    placeholder = st.empty()

    with placeholder.form(key="user_input_{0}".format(st.session_state['Form_count'])):
        with stylable_container(key="Start_dialog", css_styles=MAIN_CSS):

            st.text_input("First name", placeholder="Enter your first name", key="first_name")
            st.text_input("Last name", placeholder="Enter your last name", key="last_name")
            st.text_input("Email", placeholder="Enter your email", key="email")
            c1, _, _ = st.columns(3)
            with c1:
                st.markdown("""<div class='PolicyText'/>By clicking submit you accept our privacy policy""" , unsafe_allow_html=True)

            col1, _, col3 = st.columns(3)
            with col1:
                submit_button = st.form_submit_button("Submit", on_click=validate_user_input)
            
            with col3:
                st.link_button("See our privacy policy", "https://www.incentro.com/nl-NL/privacy-policy")

            if submit_button:
                placeholder.empty()
    return


def end_the_conversation():
    with stylable_container(key="end_questions", css_styles=MAIN_CSS):
        st.markdown("""<div class='FormHeader'/>Feedback on the conversation""" , unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.radio("Did you like this tool?", ["Yes", "No"], key="liked", index=None)

        with col2:
            st.radio("Would you like to receive a copy of the conversation per email?", ["Yes", "No"], horizontal=True, key="mail_my_result", index=None)
        
        if st.button("Submit"):
            st.session_state['Conversation_ended'] = True
            st.session_state['Ending_conversation'] = False
            st.rerun()


def conversation_ended():
    with stylable_container(key="Final_dialog", css_styles=MAIN_CSS):
        st.markdown("Thank you for your time, we hope you found this usefull")
        if st.session_state['mail_my_result'] == 'Yes':
            st.markdown("You will receive a copy of your conversation shortly, please also check your spam inbox")
        st.link_button("See other succes stories", "https://www.incentro.com/en")

def display_chat_messages():    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


# This is needed to make sure you do not lose your session variables (pretty weird, I know....)
for x,y in st.session_state.items():
    st.session_state[x] = y

# ---------------------------------- UI Main page --------------------------------------------

# Hide default UI elements
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


with stylable_container(key="main_page", css_styles=MAIN_CSS):
    st.image("https://0097f9ca.flyingcdn.com/wp-content/uploads/2022/04/Incentro-logo-2018-Orange-1024x174.png", width=200)
    st.title("Chat with Hypee!")
    st.caption("""<div class='CenterElem'/>Our chatbot 🤖 is a hyperautomation expert and loves to help you identify potential (AI) use cases. Fill in your details in the form below and get started!""", unsafe_allow_html=True)

# Initialize variables
if "Valid_input" not in st.session_state:
    print("initializing vars..")
    st.session_state['Valid_input'] = False
    st.session_state['Conversation_ended'] = False
    st.session_state['Form_count'] = 0
    st.session_state['Ending_conversation'] = False
    st.session_state['added_to_db'] = False

# Get user input before starting the chat
if st.session_state['Valid_input'] == False:
    if st.session_state['Form_count'] > 0:
        get_user_info()
        st.info("To continue, please correctly fill in this form")
    else:
        get_user_info()

# get user input at the end of the conversation
if st.session_state['Ending_conversation']:
    end_the_conversation()


# Start chat with user
with st.container():
    if st.session_state['Valid_input'] and not st.session_state['Conversation_ended'] and not st.session_state['Ending_conversation']:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Hi {0}, I'd like to help you discover your automation potential. In what branch do you work?".format(st.session_state.first_name)}]

        # Display chat messages initially
        chat_container = st.empty()
        with chat_container.container():
            display_chat_messages()

        # Place spinner element (hidden by default)
        spinner_element = st.empty()

        # End conversation
        if st.button("End conversation", type="primary"):
            st.session_state["Ending_conversation"] = True
            st.rerun()

        # Input container to ensure it stays at the bottom
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)        
        input_container = st.container()
    
        # Get user input 
        with input_container:
            if prompt := st.chat_input():
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Force refresh chat messages to include the new user message
                chat_container.empty()
                with chat_container.container():
                    display_chat_messages()

                with spinner_element:
                    with st.spinner('Thinking...'):
                        if RUN_MODE == "Production":
                            # Create new thread
                            if "Thread_id" not in st.session_state:
                                create_new_thread()
                                insert_into_DB()
                            msg = query_assistant(prompt)
                            
                        else: # Debugging:
                            if "Thread_id" not in st.session_state:
                                st.session_state["Thread_id"] = "debug_test"
                                insert_into_DB()
                            msg = "Currently just testing the user interface..."
                        
                        st.session_state.messages.append({"role": "assistant", "content": msg})

                        # Force refresh chat messages to include the new assistant message
                        chat_container.empty()
                        with chat_container.container():
                            display_chat_messages()          

                        # Clear the spinner
                        spinner_element.empty()                              

# Conversation has ended and last pop-up was filled in
if st.session_state['Conversation_ended']:
    print(st.session_state)
    if not st.session_state['added_to_db']:
        mail_conversation()
        insert_into_DB()
        st.session_state['added_to_db'] = True
    conversation_ended()
